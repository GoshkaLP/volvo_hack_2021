# Тестирование Connected Vehicle API на реальной машине
# API использовалось для получения статистики о двигателе и данных о различных диагностиках
# Информация собиралась с целью анализа и дальнейшего применения при использовании нашего проекта VOLVO TRAVEL

import requests as r


vin = 'LYVXZACACML443457'

url = 'https://api.volvocars.com/connected-vehicle/v1/vehicles/{}'.format(vin)


headers = {
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkpXVFNJR05FRENFUlQiLCJwaS5hdG0iOiI5cjdpIn0.eyJzY29wZSI6WyJjb252ZTpicmFrZV9zdGF0dXMiLCJjb252ZTpjbGltYXRpemF0aW9uX3N0YXJ0X3N0b3AiLCJjb252ZTpmdWVsX3N0YXR1cyIsImNvbnZlOmRvb3JzX3N0YXR1cyIsImNvbnZlOmVuZ2luZV9zdGFydF9zdG9wIiwiY29udmU6bG9jayIsImNvbnZlOmRpYWdub3N0aWNzX3dvcmtzaG9wIiwiY29udmU6dHJpcF9zdGF0aXN0aWNzIiwiY29udmU6ZW52aXJvbm1lbnQiLCJjb252ZTpvZG9tZXRlcl9zdGF0dXMiLCJjb252ZTpob25rX2ZsYXNoIiwiY29udmU6Y29tbWFuZF9hY2Nlc3NpYmlsaXR5IiwiY29udmU6ZW5naW5lX3N0YXR1cyIsImNvbnZlOnVubG9jayIsImNvbnZlOmNvbW1hbmRzIiwiY29udmU6bG9ja19zdGF0dXMiLCJjb252ZTp2ZWhpY2xlX3JlbGF0aW9uIiwiY29udmU6d2luZG93c19zdGF0dXMiLCJjb252ZTpuYXZpZ2F0aW9uIiwiY29udmU6dHlyZV9zdGF0dXMiLCJjb252ZTpjb25uZWN0aXZpdHlfc3RhdHVzIiwiY29udmU6ZGlhZ25vc3RpY3NfZW5naW5lX3N0YXR1cyIsImNvbnZlOndhcm5pbmdzIl0sImNsaWVudF9pZCI6ImRldmVsb3BlcnZjYXJzZG90Y29tIiwiZ3JudGlkIjoiSFRlWGFRMzRHcGFJYUUxUjZtWUtnNzFMejNTa2ZvM0oiLCJpc3MiOiJodHRwczovL3ZvbHZvaWQuZXUudm9sdm9jYXJzLmNvbSIsImF1ZCI6ImRldmVsb3BlcnZjYXJzZG90Y29tIiwiZmlyc3ROYW1lIjoiVm9sdm9jYXJzIiwibGFzdE5hbWUiOiJIYWNrYXRob24iLCJzdWIiOiJjMjkwY2RmNi01YjVjLTQ2YjEtOTg2OC1jMTZiOGE5NTQ0NTAiLCJzY29wZXMiOlsiY29udmU6YnJha2Vfc3RhdHVzIiwiY29udmU6Y2xpbWF0aXphdGlvbl9zdGFydF9zdG9wIiwiY29udmU6ZnVlbF9zdGF0dXMiLCJjb252ZTpkb29yc19zdGF0dXMiLCJjb252ZTplbmdpbmVfc3RhcnRfc3RvcCIsImNvbnZlOmxvY2siLCJjb252ZTpkaWFnbm9zdGljc193b3Jrc2hvcCIsImNvbnZlOnRyaXBfc3RhdGlzdGljcyIsImNvbnZlOmVudmlyb25tZW50IiwiY29udmU6b2RvbWV0ZXJfc3RhdHVzIiwiY29udmU6aG9ua19mbGFzaCIsImNvbnZlOmNvbW1hbmRfYWNjZXNzaWJpbGl0eSIsImNvbnZlOmVuZ2luZV9zdGF0dXMiLCJjb252ZTp1bmxvY2siLCJjb252ZTpjb21tYW5kcyIsImNvbnZlOmxvY2tfc3RhdHVzIiwiY29udmU6dmVoaWNsZV9yZWxhdGlvbiIsImNvbnZlOndpbmRvd3Nfc3RhdHVzIiwiY29udmU6bmF2aWdhdGlvbiIsImNvbnZlOnR5cmVfc3RhdHVzIiwiY29udmU6Y29ubmVjdGl2aXR5X3N0YXR1cyIsImNvbnZlOmRpYWdub3N0aWNzX2VuZ2luZV9zdGF0dXMiLCJjb252ZTp3YXJuaW5ncyJdLCJlbWFpbCI6InZvbHZvY2Fycy5oYWNrYXRob25AZ21haWwuY29tIiwiZXhwIjoxNjM1MDAxOTA4fQ.RUlIwb8nFXgVaQHlxLzakcEaY5BovrK4lKKG9HSqjmLlyHs6ANXjCWQb28ibhsovGKVHoHM6NFieejeYAC6UKQ8y3VcnfblFX5mGcAs60xQ-PV3gNoIY-DMCHYAZJTH7Rb8Jc_QYnwoIWlpfk7zroqz6IJuyN70sSK9IGebNKYoVLmj-Y0VTVRKimKSQeT0NZO7v1zNWAPuTvq95tsPelpqq9oxEzn_fR8jWv2N4Ubiutg3Oli9-Eysr6mvAXJqMFv0csIjCXKtf40PMMWQ2obxJtiaNi5792RuTGBZMBLyTyyJkruYE8PU_re2Jjqb612sHwgrB8uGxWCzXc6BGkw',
    'vcc-api-key': '73c6f8ed17af4f0190722f121792fff8'
}


with open('result.txt', 'w') as file:
    req = r.get(url, headers=headers)
    print(req.json())
    file.write('Car statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/warnings', headers=headers)
    print(req.json())
    file.write('Car warnings:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/statistics', headers=headers)
    print(req.json())
    file.write('Vehicle statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/odometer', headers=headers)
    print(req.json())
    file.write('Car odometer statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/fuel', headers=headers)
    print(req.json())
    file.write('Car fuel statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/environment', headers=headers)
    print(req.json())
    file.write('Car environment statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/engine', headers=headers)
    print(req.json())
    file.write('Car engine statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/engine-status', headers=headers)
    print(req.json())
    file.write('Car engine-status statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/diagnostics', headers=headers)
    print(req.json())
    file.write('Car last diagnostics statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/windows', headers=headers)
    print(req.json())
    file.write('Car windows statistics:\n')
    file.write(str(req.json()))
    file.write('\n')

    req = r.get(url + '/doors', headers=headers)
    print(req.json())
    file.write('Car doors statistics:\n')
    file.write(str(req.json()))
    file.write('\n')
