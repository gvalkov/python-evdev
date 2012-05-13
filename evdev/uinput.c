#include <Python.h>

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <linux/input.h>
#include <linux/uinput.h>


static int uinput_fd = -1;

static void _uinput_close(void) {
	if (uinput_fd >= 0) {
		close(uinput_fd);
		uinput_fd = -1;
	}
}


static PyObject *
uinput_open(PyObject *self, PyObject *args)
{
    struct uinput_user_dev uidev;

    __u16 vendor, product, version;
    const char* name;
    const char* uinputdev_fn;

    int ret = PyArg_ParseTuple(args, "shhhs", &name, &vendor, &product, &version, &uinputdev_fn);
    if (!ret) return NULL;

    uinput_fd = open(uinputdev_fn, O_WRONLY | O_NONBLOCK);
    if (uinput_fd < 0) {
        PyErr_SetString(PyExc_IOError, "could not open uinput device in write mode");
        return NULL;
    }

    memset(&uidev, 0, sizeof(uidev));
    strncpy(uidev.name, name, UINPUT_MAX_NAME_SIZE);
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor  = vendor;
    uidev.id.product = product;
    uidev.id.version = version;

    if (write(uinput_fd, &uidev, sizeof(uidev)) != sizeof(uidev))
        goto on_err;

	if (ioctl(uinput_fd, UI_SET_EVBIT, EV_KEY) < 0)
        goto on_err;

    int i;
	for (i=0; i<KEY_MAX && uinput_fd; i++) {
		if (ioctl(uinput_fd, UI_SET_KEYBIT, i) < 0)
            goto on_err;
	}

	if (ioctl(uinput_fd, UI_DEV_CREATE) < 0)
        goto on_err;

    return Py_BuildValue("i", uinput_fd);

    on_err:
        _uinput_close();
        PyErr_SetFromErrno(PyExc_IOError);
        return NULL;
}

static PyObject *
uinput_close(PyObject *self, PyObject *args)
{
    int fd;

    int ret = PyArg_ParseTuple(args, "i", &fd);
    if (!ret) return NULL;

    ret = ioctl(fd, UI_DEV_DESTROY);
    if (ret < 0) {
        PyErr_SetFromErrno(PyExc_IOError);
        return NULL;
    }

    return Py_BuildValue("i", 1);
}

static PyObject *
uinput_write(PyObject *self, PyObject *args)
{
    int fd, type, code, value;

    int ret = PyArg_ParseTuple(args, "iiii", &fd, &type, &code, &value);
    if (!ret) return NULL;

    struct input_event event;
    memset(&event, 0, sizeof(event));
    event.type = type;
    event.code = code;
    event.value = value;

    if (write(fd, &event, sizeof(event)) != sizeof(event)) {
        PyErr_SetString(PyExc_IOError, "error writing event to uinput device"); // @todo: elaborate
        return NULL;
    }  

    return Py_BuildValue("i", 1);
}

#define MODULE_NAME "_uinput"
#define MODULE_HELP "Python bindings for parts of linux/uinput.c"

static PyMethodDef MethodTable[] = {
    { "open",  uinput_open, METH_VARARGS,
      "Create uinput device."},

    { "close",  uinput_close, METH_VARARGS,
      "Destroy uinput device."},

    { "write",  uinput_write, METH_VARARGS,
      "Write event to uinput device."},

    { NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    MODULE_NAME,
    MODULE_HELP,
    -1,          /* m_size */
    MethodTable, /* m_methods */
    NULL,        /* m_reload */
    NULL,        /* m_traverse */
    NULL,        /* m_clear */
    NULL,        /* m_free */
};

static PyObject *
moduleinit(void)
{
    PyObject* m = PyModule_Create(&moduledef);
    if (m == NULL) return NULL;

    PyModule_AddIntConstant(m, "maxnamelen", UINPUT_MAX_NAME_SIZE);
    return m;
}

PyMODINIT_FUNC
PyInit__uinput(void)
{
    return moduleinit();
}

#else
static PyObject *
moduleinit(void)
{
    PyObject* m = Py_InitModule3(MODULE_NAME, MethodTable, MODULE_HELP);
    if (m == NULL) return NULL;

    PyModule_AddIntConstant(m, "maxnamelen", UINPUT_MAX_NAME_SIZE);
    return m;
}

PyMODINIT_FUNC
init_uinput(void)
{
    moduleinit();
}
#endif
