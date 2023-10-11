# print("connected", jvl_drive.connected)
    print(jvl_drive.identity)
    print(jvl_drive.status)
    print("Current operating mode: ", jvl_drive.get_operating_mode())
    # print("Set operating mode: ", jvl_drive.set_operating_mode())

    time.sleep(0.010)

    reg_7_response = jvl_drive.set_pos_reg_7()
    print("reg_7_response: ", reg_7_response)
    general_command = jvl_drive.issue_general_command()
    print(general_command)

    # print("Current operating mode: ", jvl_drive.get_operating_mode())
    print("Current velocity: ", jvl_drive.read_velocity())
    print("Current position: ", jvl_drive.read_current_position())

    assembly = jvl_drive.read_assembly_object()
    print("assembly: ", jvl_drive.read_assembly_object())
    print(assembly[1])
    assembly_bits = assembly[1]
    in_position = assembly_bits[4]
    print("in position: ", in_position)


    # print(UDINT.decode(b'\x01\xF4'))
    # print(UDINT.encode(500))

    # torque = jvl_drive.read_torque()
    # print("torque: ", torque)