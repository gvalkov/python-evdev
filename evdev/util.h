void print_ff_effect(struct ff_effect* effect) {
    fprintf(stderr,
            "ff_effect:\n"
            "  type: %d     \n"
            "  id:   %d     \n"
            "  direction: %d\n"
            "  trigger: (%d, %d)\n"
            "  replay:  (%d, %d)\n",
            effect->type, effect->id, effect->direction,
            effect->trigger.button, effect->trigger.interval,
            effect->replay.length, effect->replay.delay
        );

    switch (effect->type) {
    case FF_CONSTANT:
        fprintf(stderr, "  constant: (%d, (%d, %d, %d, %d))\n", effect->u.constant.level,
                effect->u.constant.envelope.attack_length,
                effect->u.constant.envelope.attack_level,
                effect->u.constant.envelope.fade_length,
                effect->u.constant.envelope.fade_level);
        break;
    }
}
