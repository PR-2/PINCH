indicator_list = {}
coil_list = {}
coil_on_list = {}
coil_off_list = {}
command_list = {"HReg_SetStatus": 0x00,
                "HReg_Status": 0x01,
                "HReg_TimeForWork": 0x03,
                "HReg_Id": 0x04,
                "HReg_Version": 0x05,
                "HReg_SetCurrent": 0x06,
                "HReg_SetVoltage": 0x07,
                "HReg_SetPower": 0x08,
                "HReg_OutputCurrent": 0x09,
                "HReg_OutputVoltage": 0x0a,
                "HReg_OutputPower": 0x0b,
                "HReg_RateOfRise": 0x0c,
                "HReg_RateOfDecay": 0x0d,
                "HReg_DelayChannel": 0x0e,
                "HReg_WorkingTime": 0x0f,
                "HReg_StatusFlag": 0x10,
                "HReg_NetFlag": 0x11,
                "HReg_MenuLanguage": 0x12,
                "HReg_InterfaceType": 0x13,
                "HReg_NetAddress": 0x14,
                "HReg_ConnectionSpeed": 0x15,
                "HReg_Parity": 0x16,
                "HReg_Temperature": 0x17}
