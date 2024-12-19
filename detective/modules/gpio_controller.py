def gpio_state_change(
    sm,queue
):  
    while True:
        if queue.empty():
            continue
        resent_gesture  = queue.get()
        print(resent_gesture,"in the gpio_state_change")
        if resent_gesture == None:
            sm.transition("default")
        sm.transition(resent_gesture)

