import os
import speech_recognition as sr
from os import path


ipaList = {'/siˈætl̩/','/kælˈkʌtə/','/ˌsæn hoʊˈzeɪ/','/ˌkæl.ɪˈfɔɹ.ni.ə/',' /ˌmɪsɪˈsɪpi/',' /nu ˈjɔɹk/','/toʊ.ki.oʊ/'}

for i in ipaList:
  os.system("py lexconvert.py --ipaConvert '{}'".format(i))