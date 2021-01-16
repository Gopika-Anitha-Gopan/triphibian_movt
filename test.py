# keyboard controls
def on_press(key):
    # character keys do not work
    instructions = {
        key.up : upthrust,
        key.down : slowDown,
        key.alt_l : yawLeft,
        key.alt_r : yawRight,
        key.ctrl_l : rollleft,
        key.ctrl_r : rollright,
        key.left : pitchup,
        key.right : pitchdown,
        key.esc : stop,
        key.space : pause

    }
    if key in instructions:
        instructions.get(key)()
    else:
        print("not a control command")
