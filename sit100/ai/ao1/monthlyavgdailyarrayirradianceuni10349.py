# arancione SOLE 6a radiazione solare giornaliera media mensile al suolo su piano orizzontale uni 10349
import math
from .concept import Measure, MeasureDerivation, months, MonthlySolarDeclination, dict2text
from .utils import log


class MonthlyAvgDailyArrayIrradianceUni10349(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_avg_daily_diffuse_horizontal_irradiance':
                    the_input_data['monthly_avg_daily_diffuse_horizontal_irradiance'],
                'monthly_avg_daily_beam_horizontal_irradiance':
                    the_input_data['monthly_avg_daily_beam_horizontal_irradiance'],
                'monthly_avg_daily_horizontal_irradiance':
                    the_input_data['monthly_avg_daily_horizontal_irradiance'],
                'latitude': the_input_data['latitude'],
                'azimuth': the_input_data['azimuth'],
                'tilt': the_input_data['tilt'],
                'albedo': the_input_data['albedo']
            }
            log("DEBUG", dict2text(self.input))
        except KeyError:
            log("ERROR", "MonthlyAvgDailyArrayIrradianceUni10349 missing input value")
        self.output = {
            'monthly_avg_daily_array_irradiance': {month: Measure("", 0) for month in months}
        }

    def validate(self):
        return True

    def compute(self):

        def horizontal_tilted_plane_irradiance_ratio(
                beam_horizontal_irradiance,
                horizontal_irradiance,
                latitude,
                azimuth,
                tilt,
                albedo,
                month_declination
        ):
            g9 = beam_horizontal_irradiance
            log("DEBUG", f"f9 = {g9}")
            f10 = horizontal_irradiance
            log("DEBUG", f"f10 = {f10}")
            f9 = f10 - g9
            log("DEBUG", f"g9 = {f9}")
            d9 = latitude
            log("DEBUG", f"d9 = {d9}")
            d11 = albedo
            log("DEBUG", f"d11 = {d11}")
            d14 = tilt
            log("DEBUG", f"d14 = {d14}")
            d15 = azimuth
            log("DEBUG", f"d15 = {d15}")
            f23 = month_declination
            log("DEBUG", f"f23 = {f23}")
            the_t = f25 = math.sin(f23 * math.pi/180)*(math.sin(d9*math.pi/180)*math.cos(d14*math.pi/180)-math.cos(d9*math.pi/180)*math.sin(d14*math.pi/180)*math.cos(d15*math.pi/180))
            log("DEBUG", f"the_t = f25 = {the_t}")
            the_u = f26 = math.cos(f23*math.pi/180)*(math.cos(d9*math.pi/180)*math.cos(d14*math.pi/180)+math.sin(d9*math.pi/180)*math.sin(d14*math.pi/180)*math.cos(d15*math.pi/180))
            log("DEBUG", f"the_u = f26 = {the_u}")
            the_v = f27 = math.cos(f23*math.pi/180)*(math.sin(d14*math.pi/180)*math.sin(d15*math.pi/180))
            log("DEBUG", f"the_v = f27 = {the_v}")
            t_h = f28 = math.sin(f23*math.pi/180)*math.sin(d9*math.pi/180)
            log("DEBUG", f"t_h = f28 = {t_h}")
            u_h = f29 = math.cos(f23*math.pi/180)*math.cos(d9*math.pi/180)
            log("DEBUG", f"u_h = f29 = {u_h}")
            u2v2h2 = f30 = f26**2+f27**2-f25**2
            log("DEBUG", f"u2v2h2 = f30 = {u2v2h2}")
            tu = f31 = f25 + f26
            log("DEBUG", f"tu = f31 = {tu}")
            omega_s = g33 = math.acos(-math.tan(d9*math.pi/180)*math.tan(f23*math.pi/180))*180/math.pi
            log("DEBUG", f"omega_s = g33 = {omega_s:.2f}")
            minusomega_s = f33 = -omega_s
            log("DEBUG", f"minusomega_s = f33 = {minusomega_s:.2f}")
            w_1 = f34 = 0 if f30<0 else min(
                2*math.atan(-f27-(f30)**0.5/(f25-f26))*180/math.pi,
                2*math.atan(-f27+(f30)**0.5/(f25-f26))*180/math.pi)
            log("DEBUG", f"w_1 = f34 = {w_1:.2f}")
            w_2 = g34 = 0 if f30<0 else max(
                2*math.atan(-f27-(f30)**0.5/(f25-f26))*180/math.pi,
                2*math.atan(-f27+(f30)**0.5/(f25-f26))*180/math.pi)
            log("DEBUG", f"w_2 = f34 = {w_2:.2f}")
            w_first = f35 = max(f33, f34) if f30>0 else (f33 if f31>0 else 0)
            log("DEBUG", f"w_first = f35 = {w_first}")
            w_second = g35 = min(g33, g34) if f30>0 else (g33 if f31>0 else 0)
            log("DEBUG", f"w_second = g35 = {w_second}")
            h_b = f37 = (f25*math.pi/180*(g35-f35)+f26*(math.sin(g35*math.pi/180)-math.sin(f35*math.pi/180))-f27*(math.cos(g35*math.pi/180)-math.cos(f35*math.pi/180)))
            log("DEBUG", f"h_b = f37 = {h_b:.2f}")
            h_bh = f38 = 2*(f28*math.pi/180*g33+f29*math.sin(g33*math.pi/180))
            log("DEBUG", f"h_bh = f38 = {h_bh}")
            r_b = f39 = 0 if (f30 <= 0 and f31 < 0) else f37/f38
            log("DEBUG", f"r_b = f39 = {r_b:.2f}")
            r = f40 = (1-f9/(f9+g9))*f39+f9/(f9+g9)*(1+math.cos(d14*math.pi/180))/2+d11*((1-math.cos(d14*math.pi/180))/2)
            # =(1-F9/(F9+G9))*F39+F9/(F9+G9)*(1+COS($D$14*PI.GRECO()/180))/2+$D$11*((1-COS($D$14*PI.GRECO()/180))/2)
            h_b = g9 * r
            h_d = f9 * r
            h = h_b + h_d
            log("DEBUG", f"r = f40 = {r:.2f}")
            log("DEBUG", f"h_b = {h_b:.2f}")
            log("DEBUG", f"h_d = {h_d:.2f}")
            log("DEBUG", f"h = {h:.2f}")
            return h

        def compute2(beam_horizontal_irradiance, horizontal_irradiance, latitude, azimuth, tilt,
                     albedo, month_declination
                     ):
            latitude_rad = math.radians(latitude_deg)
            azimuth_rad = math.radians(azimuth_deg)
            tilt_rad = math.radians(tilt_deg)
            declination_rad = math.radians(declination_deg)
            the_t = (
                    math.sin(month_declination) * (math.sin(latitude) * math.cos(tilt)
                                                   - math.cos(latitude) * math.sin(tilt) * math.cos(
                        azimuth))
            )
            log("DEBUG", f"the_t: {the_t}")
            the_u = (
                    math.cos(month_declination) * (math.cos(latitude) * math.cos(tilt)
                                                   + math.sin(latitude) * math.sin(tilt) * math.cos(
                        azimuth))
            )
            log("DEBUG", f"the_u: {the_u}")
            the_v = math.cos(month_declination) * math.sin(tilt) * math.sin(azimuth)
            log("DEBUG", f"the_v: {the_v}")
            u_v_t = the_u ** 2 + the_v ** 2 - the_t ** 2
            log("DEBUG", f"u_v_t: {u_v_t}")
            omega_s = math.acos(-math.tan(latitude) * math.tan(month_declination))
            # omega_s = 1.8
            log("DEBUG", f"omega_s: {omega_s}")
            if u_v_t > 0:
                log("DEBUG", f"u_v_t>0")
                w_a = math.atan(2 * (-the_v + math.sqrt(u_v_t)) / (the_t - the_u))
                w_b = math.atan(2 * (-the_v - math.sqrt(u_v_t)) / (the_t - the_u))
                if the_v * math.cos(w_a) > the_u * math.sin(w_a):
                    log("DEBUG", "the_v * math.cos(w_a) > the_u * math.sin(w_a)")
                    w1 = w_a
                    w2 = w_b
                else:
                    log("DEBUG", "the_v * math.cos(w_a) <= the_u * math.sin(w_a)")
                    w1 = w_b
                    w2 = w_a
                omega_1 = max(w1, -omega_s)
                omega_2 = min(w2, omega_s)
                log("DEBUG", f"omega_1: {omega_1}")
                log("DEBUG", f"omega_2: {omega_2}")
            else:
                log("DEBUG", f"u_v_t<=0")
                if the_t + the_u > 0:
                    log("DEBUG", f"the_t + the_u > 0")
                    omega_1 = - omega_s
                    omega_2 = omega_s
                else:
                    log("DEBUG", f"the_t + the_u <= 0")
                    r_b = 0.0
            if u_v_t > 0 or the_t + the_u > 0:
                log("DEBUG", f"u_v_t={u_v_t} > 0 or the_t + the_u ={the_t + the_u} > 0")
                irradiance = (
                        the_t * math.pi / 180 * (omega_2 - omega_1)
                        + the_u * (math.sin(omega_2) - math.sin(omega_1))
                        - the_v * (math.cos(omega_2) - math.cos(omega_1))
                )
                beam_irradiance = 2 * (the_t * math.pi / 180 * omega_s + the_u * math.sin(omega_s))
                r_b = irradiance / beam_irradiance
            else:
                log("DEBUG", f"u_v_t={u_v_t} <= 0 and the_t + the_u ={the_t + the_u} <= 0")
            log("DEBUG", f"r_b: {r_b}")
            log("DEBUG", f"(1 - beam_horizontal_irradiance / horizontal_irradiance): {1 - beam_horizontal_irradiance / horizontal_irradiance}")
            log("DEBUG", f"1 - beam_horizontal_irradiance / horizontal_irradiance) * r_b: {(1 - beam_horizontal_irradiance / horizontal_irradiance) * r_b}")
            log("DEBUG", f"r_b: {r_b}")
            log("DEBUG", f"albedo * (1 - math.cos(tilt)) / 2: {albedo * (1 - math.cos(tilt)) / 2}")
            r = (
                    (1 - beam_horizontal_irradiance / horizontal_irradiance) * r_b
                    + beam_horizontal_irradiance / horizontal_irradiance * (1 + math.cos(tilt)) / 2
                    + albedo * (1 - math.cos(tilt)) / 2
            )
            log("DEBUG", f"r: {r}")
            monthly_avg_daily_array_irradiance = r * horizontal_irradiance
            log("DEBUG", f"monthly_avg_daily_array_irradiance = {monthly_avg_daily_array_irradiance}")
            return monthly_avg_daily_array_irradiance

        monthly_solar_declinations = MonthlySolarDeclination()
        for month in months:
            # diffuse_horizontal_irradiance = self.input['monthly_avg_daily_diffuse_horizontal_irradiance'].value
            beam_horizontal_irradiance_measure = self.input['monthly_avg_daily_beam_horizontal_irradiance'][month]
            log("DEBUG", f"{month} beam horizontal irradiance: {beam_horizontal_irradiance_measure.value}")
            beam_horizontal_irradiance = beam_horizontal_irradiance_measure.value
            horizontal_irradiance = self.input['monthly_avg_daily_horizontal_irradiance'][month].value
            log("DEBUG", f"{month} horizontal irradiance: {horizontal_irradiance}")
            latitude = self.input['latitude'].value
            azimuth = self.input['azimuth'].value
            tilt = self.input['tilt'].value
            albedo = self.input['albedo'].value
            declination = monthly_solar_declinations.get_solar_declination(month)
            monthly_avg_daily_array_irradiance_value = horizontal_tilted_plane_irradiance_ratio(
                beam_horizontal_irradiance,
                horizontal_irradiance,
                latitude,
                azimuth,
                tilt,
                albedo,
                declination
            )
            log("DEBUG", f"{month} irradiance: {monthly_avg_daily_array_irradiance_value}")
            self.output['monthly_avg_daily_array_irradiance'][month] = Measure("kWh/m2/giorno", round(
                monthly_avg_daily_array_irradiance_value, 2))


if __name__ == '__main__':
    the_target = MonthlyAvgDailyArrayIrradianceUni10349({
        "monthly_avg_daily_diffuse_horizontal_irradiance":
            {
                "GEN": Measure("kWh/m2/giorno", 2.70),
                "FEB": Measure("kWh/m2/giorno", 4.10),
                "MAR": Measure("kWh/m2/giorno", 2.41),
                "APR": Measure("kWh/m2/giorno", 1.53),
                "MAG": Measure("kWh/m2/giorno", 2.00),
                "GIU": Measure("kWh/m2/giorno", 6.27),
                "LUG": Measure("kWh/m2/giorno", 3.65),
                "AGO": Measure("kWh/m2/giorno", 5.50),
                "SET": Measure("kWh/m2/giorno", 4.60),
                "OTT": Measure("kWh/m2/giorno", 6.66),
                "NOV": Measure("kWh/m2/giorno", 5.70),
                "DIC": Measure("kWh/m2/giorno", 6.94)
            },
        "monthly_avg_daily_beam_horizontal_irradiance": {
            "GEN": Measure("kWh/m2/giorno", 1.70),
            "FEB": Measure("kWh/m2/giorno", 3.10),
            "MAR": Measure("kWh/m2/giorno", 1.41),
            "APR": Measure("kWh/m2/giorno", 0.53),
            "MAG": Measure("kWh/m2/giorno", 1.00),
            "GIU": Measure("kWh/m2/giorno", 5.27),
            "LUG": Measure("kWh/m2/giorno", 2.65),
            "AGO": Measure("kWh/m2/giorno", 4.50),
            "SET": Measure("kWh/m2/giorno", 3.60),
            "OTT": Measure("kWh/m2/giorno", 5.66),
            "NOV": Measure("kWh/m2/giorno", 4.70),
            "DIC": Measure("kWh/m2/giorno", 5.94)
            },
        'monthly_avg_horizontal_irradiance': {
            "GEN": Measure("kWh/m2/giorno", 2.70),
            "FEB": Measure("kWh/m2/giorno", 4.10),
            "MAR": Measure("kWh/m2/giorno", 2.41),
            "APR": Measure("kWh/m2/giorno", 1.53),
            "MAG": Measure("kWh/m2/giorno", 2.00),
            "GIU": Measure("kWh/m2/giorno", 6.27),
            "LUG": Measure("kWh/m2/giorno", 3.65),
            "AGO": Measure("kWh/m2/giorno", 5.50),
            "SET": Measure("kWh/m2/giorno", 4.60),
            "OTT": Measure("kWh/m2/giorno", 6.66),
            "NOV": Measure("kWh/m2/giorno", 5.70),
            "DIC": Measure("kWh/m2/giorno", 6.94)
            },
        'latitude': Measure("°", 41.9028),
        'azimuth': Measure("°", 15.0),
        'tilt': Measure("°", 12.0),
        'albedo': Measure("", 0.20),
        'month_declination': Measure("°", 15.0)
        # "longitude": Measure("°", 12.4964)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
