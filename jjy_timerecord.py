#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import time
from smbus import SMBus

JJY_MARKER = -1
JJY_MARKER_LAST = -2

SI5351A_DEV_ADDR = 0x60

REG_DEV_STATUS = 0x00
REG_OUTPUT_EN_CTRL = 0x03
REG_OUTPUT_EN_CTRL_MASK = 0x09
REG_PLL_INPUT_SOURCE = 0x0F
REG_CLK0_CTRL = 0x10
REG_CLK1_CTRL = 0x11
REG_CLK2_CTRL = 0x12
REG_CLK0_CLK3_DISABLE_STATE = 0x18

REG_MS_NA_BASE = 0x1A
REG_MS0_BASE = 0x2A
REG_MS1_BASE = 0x32
REG_MS2_BASE = 0x3A
OFFSET_MS_P3_1 = 0
OFFSET_MS_P3_0 = 1
OFFSET_MS_R_P1_2 = 2
OFFSET_MS_P1_1 = 3
OFFSET_MS_P1_0 = 4
OFFSET_MS_P3_P2_2 = 5
OFFSET_MS_P2_1 = 6
OFFSET_MS_P2_0 = 7

REG_SS_BASE = 0x95
RANGE_SS = 13
REG_VCXO_BASE = 0xA2
RANGE_VCXO = 3
REG_CLK0_INIT_PHASE_OFFSET = 0xA5
REG_CLK1_INIT_PHASE_OFFSET = 0xA6
REG_CLK2_INIT_PHASE_OFFSET = 0xA7
REG_PLL_RESET = 0xB1
PLLA_RST = ((0x1 << 5) & 0xFF)
PLLB_RST = ((0x1 << 7) & 0xFF)
REG_XTAL_CL = 0xB7
REG_FANOUT_EN = 0xBB

# PLL0 : 450MHz
MS_NA_P1 = 1792
MS_NA_P2 = 0
MS_NA_P3 = 1

# Multisynth0 : 60kHz
MS0_P1 = 119488
MS0_P2 = 0
MS0_P3 = 1
MS0_R = 3 # 2^3=8

# Multisynth1 : 40kHz
MS1_P1 = 179488
MS1_P2 = 0
MS1_P3 = 1
MS1_R = 3 # 2^3=8

class Si5351A:
    def __init__(self):
        self.device_init()

    def device_init(self):
        self.bus = SMBus(1)

        # Disable Outputs
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_OUTPUT_EN_CTRL, 0x55)

        # Powerdown all output drivers
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK0_CTRL, 0x80)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK1_CTRL, 0x80)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK2_CTRL, 0x80)

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK0_CLK3_DISABLE_STATE, 0x00)

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_PLL_INPUT_SOURCE, 0x00)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_XTAL_CL, 0x92)

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P3_1, ((MS_NA_P3 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P3_0, ((MS_NA_P3 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_R_P1_2, ((MS_NA_P1 >> 16) & 0x03))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P1_1, ((MS_NA_P1 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P1_0, ((MS_NA_P1 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P3_P2_2, (((MS_NA_P3 >> 12) & 0xF0) | ((MS_NA_P2 >> 16) & 0x0F)))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P2_1, ((MS_NA_P2 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS_NA_BASE + OFFSET_MS_P2_0, ((MS_NA_P2 >> 0) & 0xFF))

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P3_1, ((MS0_P3 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P3_0, ((MS0_P3 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_R_P1_2, (((MS0_R << 4) & 0xF0) | (MS0_P1 >> 16) & 0x03))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P1_1, ((MS0_P1 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P1_0, ((MS0_P1 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P3_P2_2, (((MS0_P3 >> 12) & 0xF0) | ((MS0_P2 >> 16) & 0x0F)))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P2_1, ((MS0_P2 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS0_BASE + OFFSET_MS_P2_0, ((MS0_P2 >> 0) & 0xFF))

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P3_1, ((MS1_P3 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P3_0, ((MS1_P3 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_R_P1_2, (((MS0_R << 4) & 0xF0) | (MS1_P1 >> 16) & 0x03))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P1_1, ((MS1_P1 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P1_0, ((MS1_P1 >> 0) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P3_P2_2, (((MS1_P3 >> 12) & 0xF0) | ((MS1_P2 >> 16) & 0x0F)))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P2_1, ((MS1_P2 >> 8) & 0xFF))
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_MS1_BASE + OFFSET_MS_P2_0, ((MS1_P2 >> 0) & 0xFF))

        # Reset PLL
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_PLL_RESET, (PLLA_RST | PLLB_RST))

        # Setup CLKx
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK0_INIT_PHASE_OFFSET, 0x00)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK1_INIT_PHASE_OFFSET, 0x00)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK2_INIT_PHASE_OFFSET, 0x00)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_FANOUT_EN, 0x00)

        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK0_CTRL, 0x0F)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK1_CTRL, 0x8F)
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_CLK2_CTRL, 0x8F)

    def clk0_ctrl(self, enable):
        _reg = 0xFE if enable else 0xFF
        self.bus.write_byte_data(SI5351A_DEV_ADDR, REG_OUTPUT_EN_CTRL, _reg)


class JJYTimerecord:
    def convert_minute(self, minute):
        self.min_bits = []
        _minute_10, _minute_1 = divmod(minute, 10)
        self.min_bits.append((_minute_10 >> 2) & 0x1)
        self.min_bits.append((_minute_10 >> 1) & 0x1)
        self.min_bits.append((_minute_10 >> 0) & 0x1)
        self.min_bits.append(0)
        self.min_bits.append((_minute_1 >> 3) & 0x1)
        self.min_bits.append((_minute_1 >> 2) & 0x1)
        self.min_bits.append((_minute_1 >> 1) & 0x1)
        self.min_bits.append((_minute_1 >> 0) & 0x1)
        self.min_parity = sum(self.min_bits) % 2

    def convert_hour(self, hour):
        self.hour_bits = []
        _hour_10, _hour_1 = divmod(hour, 10)
        self.hour_bits.append((_hour_10 >> 1) & 0x1)
        self.hour_bits.append((_hour_10 >> 0) & 0x1)
        self.hour_bits.append(0)
        self.hour_bits.append((_hour_1 >> 3) & 0x1)
        self.hour_bits.append((_hour_1 >> 2) & 0x1)
        self.hour_bits.append((_hour_1 >> 1) & 0x1)
        self.hour_bits.append((_hour_1 >> 0) & 0x1)
        self.hour_parity = sum(self.hour_bits) % 2

    def convert_day(self, day):
        self.day_100_bits = []
        self.day_10_bits = []
        self.day_1_bits = []
        _day_100, _day_10 = divmod(day, 100)
        _day_10, _day_1 = divmod(_day_10, 10)
        self.day_100_bits.append((_day_100 >> 1) & 0x1)
        self.day_100_bits.append((_day_100 >> 0) & 0x1)
        self.day_10_bits.append((_day_10 >> 3) & 0x1)
        self.day_10_bits.append((_day_10 >> 2) & 0x1)
        self.day_10_bits.append((_day_10 >> 1) & 0x1)
        self.day_10_bits.append((_day_10 >> 0) & 0x1)
        self.day_1_bits.append((_day_1 >> 3) & 0x1)
        self.day_1_bits.append((_day_1 >> 2) & 0x1)
        self.day_1_bits.append((_day_1 >> 1) & 0x1)
        self.day_1_bits.append((_day_1 >> 0) & 0x1)

    def convert_year(self, year):
        self.year_bits = []
        _year_10, _year_1 = divmod((year % 100), 10)
        self.year_bits.append((_year_10 >> 3) & 0x1)
        self.year_bits.append((_year_10 >> 2) & 0x1)
        self.year_bits.append((_year_10 >> 1) & 0x1)
        self.year_bits.append((_year_10 >> 0) & 0x1)
        self.year_bits.append((_year_1 >> 3) & 0x1)
        self.year_bits.append((_year_1 >> 2) & 0x1)
        self.year_bits.append((_year_1 >> 1) & 0x1)
        self.year_bits.append((_year_1 >> 0) & 0x1)

    def convert_wday(self, wday):
        self.wday_bits = []
        self.wday_bits.append((wday >> 2) & 0x1)
        self.wday_bits.append((wday >> 1) & 0x1)
        self.wday_bits.append((wday >> 0) & 0x1)

    def get_next_timerecord(self, nexttime):
        self.convert_minute(nexttime.minute)
        self.convert_hour(nexttime.hour)
        self.convert_day(nexttime.toordinal() - datetime.date(nexttime.year, 1, 1).toordinal() + 1)
        self.convert_year(nexttime.year)
        self.convert_wday(nexttime.isoweekday() % 7)

        self.bits_list = []
        self.bits_list.append(JJY_MARKER)
        self.bits_list.extend(self.min_bits)
        self.bits_list.extend([JJY_MARKER, 0, 0])
        self.bits_list.extend(self.hour_bits)
        self.bits_list.extend([JJY_MARKER, 0, 0])
        self.bits_list.extend(self.day_100_bits)
        self.bits_list.append(0)
        self.bits_list.extend(self.day_10_bits)
        self.bits_list.append(JJY_MARKER)
        self.bits_list.extend(self.day_1_bits)
        self.bits_list.extend([0, 0, self.hour_parity, self.min_parity, 0, JJY_MARKER, 0])
        if nexttime.minute not in [15, 45]:
            self.bits_list.extend(self.year_bits)
            self.bits_list.append(JJY_MARKER)
            self.bits_list.extend(self.wday_bits)
        else:
            self.bits_list.extend([0, 0, 0, 0, 0, 0, 0, 0, JJY_MARKER, 0, 0, 0])
        self.bits_list.extend([0, 0, 0, 0, 0, 0, JJY_MARKER_LAST])

        return self.bits_list

def send_bit(clk, bit):
    if bit == -1: # marker
        clk.clk0_ctrl(True)
        time.sleep(0.2)
        clk.clk0_ctrl(False)
        time.sleep(0.799)
    elif bit == 0: # 0
        clk.clk0_ctrl(True)
        time.sleep(0.799)
        clk.clk0_ctrl(False)
        time.sleep(0.2)
    elif bit == 1: # 1
        clk.clk0_ctrl(True)
        time.sleep(0.499)
        clk.clk0_ctrl(False)
        time.sleep(0.5)
    else:   # marker(non sleep)
        clk.clk0_ctrl(True)
        time.sleep(0.2)
        clk.clk0_ctrl(False)

def main():
    _clk = Si5351A()

    _jjy = JJYTimerecord()
    _1min = datetime.timedelta(minutes=1)

    while True:
        _nexttime = datetime.datetime.now() + _1min
        _bits_list = _jjy.get_next_timerecord(_nexttime)
        #print(_nexttime)
        #print(_bits_list)
        _now = datetime.datetime.now()
        #print(_now)
        if _nexttime.minute == _now.minute:
            #print('continue')
            continue
        time.sleep(60 - (_now.second + (_now.microsecond / 1000000.0))) # 0秒になるまで待つ
        for i in _bits_list:
            send_bit(_clk, i)

if __name__ == '__main__':
    main()
