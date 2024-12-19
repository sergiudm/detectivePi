def gpio_state_change(
    sm
):
    global resent_gesture
    if resent_gesture == None:
        sm.transition("default")
    sm.transition(resent_gesture)

