import Drivers.Terminal.iCDs

class icd_strucks:
    def __init__(self):
        self.iCD = Drivers.Terminal.iCDs

        self.strFormats = {
            "setTxFreqMsg": '=BQQ',
            "setRxFreqMsg": '=BQQQ',
            "setLmxTxFreqMsg": '=BBd',
            "getReportMsg": '=BB',
            "modemConfigMsg": '=Bifii',
            "Admv4420FreqMsg": '=BBdf',
            "ADMV4420RegMsg": '=BBHB',
            "MAX2112RegMsg": '=BBBB',
            "antPwrCtrlMsg": '=BBB',
            "clkDacMsg": '=BH',
            "Lmx2592FreqMsg": '=BBd',
            "regReadWriteMsg": '=BBBI',
            "ADMV1013RegMsg": '=BBBH',
            "phaseSetDynamicMsg": '=BBdddB',
            "PICReadWriteMsg": '=BBBH',
            "MxFEAxiRegMsg": '=BBII',
            "modemRegCommandMsg": '=BBBI',
            "modemParamMsg": '=BffBf',
            "dataStatusRepMsg": '=BIIIIIBHI',
            "batParamRep": '=BHHhhHHHHHHHHHHHHH',
            "dynPointParamMsg": '=BffffffBdcdcdffffffffffffffffffff',
            "PointAntStruct": '=BffffffbffBfiiiff',
            "ad9364OpRepMsg": '=cBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBffffffffffffiiBBBdddBBBBBBBBBBBBBBBBBBBBBffdddBBBBBBBBBBfffIBB'
        }

        # old units structs-------------------------------------------------
        self.setTxFreqMsg = {
            "opcode": 2,
            "rfBandWith": 15000000,
            "txFreq": 3000000000}

        self.setRxFreqMsg = {
            "opcode": 3,
            "rfBandWith": 15 * 1000000,
            "sampleRate": int(self.iCD.RX_CATALINA_SAMPLE_RATE * self.iCD.MHZ),
            "rxFreq": 1400 * 1000000}

        # new units --------------------------------------------------------
        self.setLmxTxFreqMsg = {
            "opcode": 160,
            "cmnd": 0,
            "txFreq": 29098
        }
        
        self.getReportMsg = {
            "opcode": 0x63,
            "reqMsgOpcode": 0xff
        }

        self.modemConfigMsg = {
            "opcode": self.iCD.IOT_MODEM_CONFIG_TX, # 119 is for Rx, 138 is for Tx
            "modType": self.iCD.MOD_QPSK,
            "symRate": 40,
            "spreadFact": 20,
            "preIntrvl": 50
        }

        # ------------------GENERAL----------------------------
        ##------------------RX Configuration - LBand-----------
        self.ad9364OpRepMsg = {
            "opcode": 0,
            "ensm_mode1": 0,
            "ensm_mode2": 0,
            "ensm_mode3": 0,
            "ensm_mode4": 0,
            "ensm_mode5": 0,
            "ensm_mode6": 0,
            "ensm_mode7": 0,
            "ensm_mode8": 0,
            "ensm_mode9": 0,
            "ensm_mode10": 0,
            "ensm_mode11": 0,
            "ensm_mode12": 0,
            "ensm_mode13": 0,
            "ensm_mode14": 0,
            "ensm_mode15": 0,
            "ensm_mode16": 0,
            "ensm_mode17": 0,
            "calib_mode1": 0,
            "calib_mode2": 0,
            "calib_mode3": 0,
            "calib_mode4": 0,
            "calib_mode5": 0,
            "calib_mode6": 0,
            "calib_mode7": 0,
            "calib_mode8": 0,
            "calib_mode9": 0,
            "calib_mode10": 0,
            "calib_mode11": 0,
            "calib_mode12": 0,
            "calib_mode13": 0,
            "calib_mode14": 0,
            "calib_mode15": 0,
            "calib_mode16": 0,
            "calib_mode17": 0,
            "calib_mode18": 0,
            "calib_mode19": 0,
            "calib_mode20": 0,
            "calib_mode21": 0,
            "calib_mode22": 0,
            "rateGoverner1":0,
            "rateGoverner1": 0,
            "rateGoverner2": 0,
            "rateGoverner3": 0,
            "rateGoverner4": 0,
            "rateGoverner5": 0,
            "rateGoverner6": 0,
            "rateGoverner7": 0,
            "rateGoverner8": 0,
            "rateGoverner9": 0,
            "rateGoverner10": 0,
            "rateGoverner11": 0,
            "rateGoverner12": 0,
            "rxRates1": 0,
            "rxRates2": 0,
            "rxRates3": 0,
            "rxRates4": 0,
            "rxRates5": 0,
            "rxRates6": 0,
            "txRates1": 0,
            "txRates2": 0,
            "txRates3": 0,
            "txRates4": 0,
            "txRates5": 0,
            "txRates6": 0,
            "dcxoFine": 0,
            "dcxoCoarse": 0,
            "txFirEn": 0,
            "rxFirEn": 0,
            "txRxFirEn": 0,
            "rxRfBandwith": 0,
            "rxSamplFreq": 0,
            "rxLofreq": 0,
            "rxGainCtrl1": 0,
            "rxGainCtrl2": 0,
            "rxGainCtrl3": 0,
            "rxGainCtrl4": 0,
            "rxGainCtrl5": 0,
            "rxGainCtrl6": 0,
            "rxGainCtrl7": 0,
            "rxGainCtrl8": 0,
            "rxGainCtrl9": 0,
            "rxGainCtrl10": 0,
            "rxGainCtrl11": 0,
            "rxRfPort1": 0,
            "rxRfPort2": 0,
            "rxRfPort3": 0,
            "rxRfPort4": 0,
            "rxRfPort5": 0,
            "rxRfPort6": 0,
            "rxRfPort7": 0,
            "rxRfPort8": 0,
            "rxRfPort9": 0,
            "rxRfPort10": 0,
            "rxGain": 0,
            "rssi": 0,
            "txRfBandwith": 0,
            "txSamplFreq": 0,
            "txLofreq": 0,
            "txRfPort1": 0,
            "txRfPort2": 0,
            "txRfPort3": 0,
            "txRfPort4": 0,
            "txRfPort5": 0,
            "txRfPort6": 0,
            "txRfPort7": 0,
            "txRfPort8": 0,
            "txRfPort9": 0,
            "txRfPort10": 0,
            "txGain": 0,
            "modemSnr": 0,
            "modemEstFreq": 0,
            "modemRegData": 0,
            "ver": 0,
            "rev": 0
        }
        ## -----------------REGISTERS--------------------------
        self.modemRegCommandMsg = {
            "opcode": self.iCD.ARM_REGISTER,  # option B: MODEM_REGISTER
            "cmd": self.iCD.WRITE, # for READ is READ
            "addr": 255,  # 0xff
            "data": 65535  # 0xffff for READ this is 0
        }

        self.modemParamMsg = {
            "opcode": 0, # 0x26
            "modemSnr": 0, # EbN0 = modemSnr / 16
            "modemEstFreq": 0,
            "modemSync": 0,
            "modemEnN0Rem": 0 # freq offset = ((modemParamMsg.modemEstFreq / (Math.Pow(2, 16))) * 40000).ToString("N2")
        }

        self.dataStatusRepMsg = {
            "opcode": 0,
            "sentMsgCnt": 0,
            "rcvMsgCnt": 0,
            "crcErrCnt": 0,
            "properPackCnt": 0,
            "dropPackCnt": 0,
            "function": 0,
            "regDataRead": 0,
            "rcvBytesCnt": 0
        }

        self.batParamRep = {
            "opcode": 0,
            "tempK": 0,
            "voltage": 0,
            "current": 0,
            "avgCurrent": 0,
            "remainingCapacity": 0,
            "fullChargeCapacity": 0,
            "runTimeToEmpty": 0,
            "avgTimeToEmpty": 0,
            "avgTimeToFull" :0,  # 0...65534 - remain predicted time to full charged, 65535 - battery is not being charged.
            "chargingCurrent": 0,
            "chargingVoltage": 0,
            "batteryStatus": 0 ,# See bq20z95_tech_manual.pdf page 80.
            "designCapacity":0 , # // Design capacity in units of mAh.
            # ------Calculated individual cell voltages, in mV. -------
            "cellVoltage3": 0,
            "cellVoltage2":0,
            "cellVoltage1":0,
            "digTemp" : 0   # this is needed for digital temp
        }

        # ------------------ANTENNA POINTING----------------------------
        ##--------------------------GPS SENSOR--------------------------
        self.dynPointParamMsg = {
            "opcode": 0, # OPCODE 0xCE
            "intYaw": 0,
            "intPitch": 0,
            "intRoll": 0,
            "extYaw": 0,
            "extPitch": 0,
            "extRoll": 0,
            "status": 0, # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix
            "latitude": 0,
            "nsIndicator": 0, # North/South Indicator.
            "longitude": 0,
            "ewIndicator": 0, # East/West Indicator.
            "altitude": 0,
            # === Belong to  DynamicMT\ATENNA POINTING folder ===
            "angHor": 0,
            "angVer": 0,
            "angEl": 0,
            "angAz": 0,
            # ===================================================
            "trackStat": 0,
            "rssiAzOff" : 0,
            "rssiElOff": 0,
            "northYawOff": 0,
            "dummy1": 0,
            "dummy2": 0,
            "dummy3": 0,
            "dummy4": 0,
            "dummy5": 0,
            "dummy6": 0,
            "dummy7": 0,
            "dummy8": 0,
            "dummy9": 0,
            "dummy10": 0,
            "dummy11": 0
        }

        ##-------------IMU SENSORS - ROLL, PITCH, YAW ------------------
        self.PointAntStruct = {
            "opcode": 0,  # OPCODE 0xC9
            "imuRoll": 0,
            "imuPitch": 0,
            "imuYaw": 0,
            "Longitude": 0,
            "Latitude": 0,
            "Altitude": 0,
            "gpsStatus": 0,
            "mta_hor": 0,
            "mta_ver": 0,
            "memsCalib": 0,
            "heading": 0,
            "mag_X": 0,
            "mag_Y": 0,
            "mag_Z": 0,
            "EbNo": 0,
            "FreqEst": 0
        }
        # ------------------------DynamicMT------------------------------
        ##--------------------------ATENNA POINTING-----------------------
        '''See dynPointParamMsg in ANTENNA POINTING SECTION . '''

        #------------------Gen2------------------------
        ##--------------------RX STATIC----------------
        ###---------------------ADMV4420---------------
        self.Admv4420FreqMsg = {
            "opcode" : self.iCD.ADMV4420_FREQ_SET,
            "cmnd" : self.iCD.SPI_WRITE,
            "rfFreq": 20346.5,
            "ifFreq": 2226
        }

        self.ADMV4420RegMsg = {
            "opcode": self.iCD.ADMV4420_REG_SET_GET,
            "cmd" : self.iCD.SPI_WRITE, #for reading use SPI_READ
            "addr": 65535, #0xffff
            "data": 255    #0xff
        }

        ###---------------------MAX2112---------------
        self.MAX2112RegMsg = {
            "opcde": self.iCD.MAX2112_REG_SET_GET,
            "cmd": self.iCD.SPI_WRITE, #for reading use SPI_READ
            "addr": 255,  # 0xff
            "data": 255  # 0xff
        }

        ##--------------------PWR MODE----------------
        self.antPwrCtrlMsg = {
            "opcode": self.iCD.ANTENNA_PWR_CTRL,
            "antType": 0, # 0 is for RX, 4 is for TX
            "pwrMode": 0, #0 is for OFF, 1 is SAVE, 2 is ON
        }

        ##--------------------CLOCK VOLTAGE DAC----------------
        self.clkDacMsg = {
            "opcode": self.iCD.CLK_DAC_SET,
            "val": 65535 #0xffff
        }

        ##--------------------TX STATIC----------------
        ###---------------------LMX2592----------------
        self.Lmx2592FreqMsg = {
            "opcode": self.iCD.LMX2592_FREQ_SET,
            "cmnd": self.iCD.SPI_WRITE,
            "val": 29098
        }
        self.regReadWriteMsg = {
            "opcode": self.iCD.LMX2592_REG_SET_GET,
            "cmd": self.iCD.SPI_WRITE,
            "addr": 255,  # 0xff
            "data": 65535  # 0xffff
        }

        ###---------------------ADMV1013----------------
        self.ADMV1013RegMsg = {
            "opcode": self.iCD.ADMV1013_REG_SET_GET,
            "cmd": self.iCD.SPI_WRITE, #for reading use SPI_READ
            "addr": 255,  # 0xff
            "data": 65535  # 0xffff
        }

        ###---------------------DYNAMIC ANTENNA----------------
        self.phaseSetDynamicMsg = {
            "opcode": self.iCD.PHASE_DYNAMIC_SET,
            "rtx": 0, # 0 is for RX, 1 is for TX
            "freqRf": 29098,
            "verShift": 0,
            "horShift": 0,
            "leftRight": 0 # 0 is for RIGHT, 1 is for LEFT
        }
        ###---------------------PIC-------------------------
        self.PICReadWriteMsg = {
            "opcode": self.iCD.PIC_REG_SET_GET,
            "cmd":self.iCD.SPI_WRITE,
            "addr": 255,  # 0xff
            "data": 255  # 0xffff
        }

        ##--------------------PA Turn OFF/ON----------------
        self.MxFEAxiRegMsg = {
            "opcode": self.iCD.MICROBLAZE_REGFILE_SET,
            "cmd": self.iCD.SPI_WRITE,
            "addr": 0x17,
            "data": 0x7     # 0x7 is ON, 0x3 is OFF
        }
        # -----------------------------------------------------------------------

