import sombras_em_coordernadas_polares
import numpy as np

def test_angulo_solar_equinocio():
    # Teste para o cálculo do ângulo solar no equador ao meio-dia no equinocio de primavera (21 de março)
    dia = 21
    mes = 3
    hora = 12
    latitude = 0  # Equador

    dia_do_ano = sombras_em_coordernadas_polares.obter_dia_do_ano(dia, mes)
    declinacao = sombras_em_coordernadas_polares.declinacao_solar(dia_do_ano)
    angulo_horario = sombras_em_coordernadas_polares.angulo_horario(hora)
    angulo_solar_calculado = sombras_em_coordernadas_polares.angulo_solar(declinacao, latitude, angulo_horario)

    # O ângulo solar no equador ao meio-dia do equinócio de primavera deve ser aproximadamente 90 graus
    assert np.isclose(angulo_solar_calculado, 90, atol=1), f"Ângulo solar calculado: {angulo_solar_calculado}"

def __main__():
    test_angulo_solar_equinocio()
    print("Teste do ângulo solar passou com sucesso!")

if __name__ == "__main__":
    __main__()