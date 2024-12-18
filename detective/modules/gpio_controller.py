def gpio_state_change(
    sm
):
    global resent_gesture
    sm.transition(resent_gesture)

