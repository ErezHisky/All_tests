import pywifi
import time
from pywifi import const


class Wifi_Connection:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.unit_net_name = ''
        self.unit_net_exist = False

    def find_terminal(self):
        self.iface = self.wifi.interfaces()[0]
        self.iface.scan()
        time.sleep(8)
        for n in self.iface.scan_results():
            if "Static" in n.ssid or "EREZ" in n.ssid: # Dynamic
                self.unit_net_name = n.ssid
                self.unit_net_exist = True
                break

    def wifi_connect_to_terminal(self):
        '''
        checks if Static ro Dynamic terminal wifi exist and try to connect.
        :return:
        '''
        self.find_terminal()
        if self.unit_net_exist:
            self.iface.disconnect()
            time.sleep(1)
            assert self.iface.status() in \
                   [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

            profile = pywifi.Profile()
            profile.ssid = self.unit_net_name  # 'Hisky_Static_Terminal_2'
            profile.auth = const.AUTH_ALG_OPEN
            # profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = ''  # 'H15ky@T0!'

            self.iface.remove_all_network_profiles()
            tmp_profile = self.iface.add_network_profile(profile)

            self.iface.connect(tmp_profile)
            time.sleep(10)
            assert self.iface.status() == const.IFACE_CONNECTED
            if self.unit_net_exist:
                return self.unit_net_name
        else:
            print("wifi with name searched wasn't found.")


if __name__=="__main__":
    myWifi = Wifi_Connection()
    try:
        net = myWifi.wifi_connect_to_terminal()
        print(f"conneted to {net}")
    except:
        pass
    print('Done')

