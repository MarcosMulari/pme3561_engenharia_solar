import numpy as np
import matplotlib.pyplot as plt

def obter_dia_do_ano(dia, mes):
    # Cálculo do dia do ano a partir do dia e mês
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dia_do_ano = sum(dias_por_mes[:mes - 1]) + dia
    return dia_do_ano

def declinacao_solar(dia):
    # Cálculo da declinação solar em graus
    declinacao = 23.45 * np.sin(np.radians(360 * (284 + dia) / 365))
    return declinacao


def angulo_horario(hora):
    return (hora - 12) * 15


def angulo_solar(declinacao_solar, latitude, angulo_horario):
    # Cálculo do ângulo solar em graus
    angulo = np.arcsin(np.sin(np.radians(latitude)) * np.sin(np.radians(declinacao_solar)) +
                       np.cos(np.radians(latitude)) * np.cos(np.radians(declinacao_solar)) *
                       np.cos(np.radians(angulo_horario)))
    return np.degrees(angulo)

def tamanho_da_sombra_no_plano_horizontal(altura_objeto, angulo_solar):
    # Cálculo do comprimento da sombra
    sombra = altura_objeto / np.tan(np.radians(angulo_solar))
    return sombra

def remover_outliers_sombra(sombras, metodo='iqr', limite_iqr=1.5):
    # Remove outliers das sombras usando IQR
    if metodo == 'iqr':
        Q1 = np.percentile(sombras, 25)
        Q3 = np.percentile(sombras, 75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - limite_iqr * IQR
        limite_superior = Q3 + limite_iqr * IQR
        
        # Retorna máscara de índices válidos
        mascara = (sombras >= limite_inferior) & (sombras <= limite_superior)
        return mascara
    
    elif metodo == 'percentil':
        # Remove valores acima do percentil 95
        limite = np.percentile(sombras, 95)
        mascara = sombras <= limite
        return mascara
    
    elif metodo == 'desvio_padrao':
        # Remove valores além de 3 desvios padrão
        media = np.mean(sombras)
        desvio = np.std(sombras)
        mascara = np.abs(sombras - media) <= 3 * desvio
        return mascara
    
    else:
        raise ValueError("Método deve ser 'iqr', 'percentil' ou 'desvio_padrao'")

def calcular_dados_solares(dia, latitude, horas):
    # Calcula os dados solares para um conjunto de horas
    declinacao = declinacao_solar(dia)
    angulos_horarios = angulo_horario(horas)
    angulos_solares = angulo_solar(declinacao, latitude, angulos_horarios)
    return declinacao, angulos_horarios, angulos_solares

def obter_nascer_poente(dia, latitude):
    # Calcula os horários de nascer e pôr do sol
    horas = np.arange(0, 24, 0.1)
    declinacao, angulos_horarios, angulos_solares = calcular_dados_solares(dia, latitude, horas)
    
    # Encontrar índices onde o sol está acima do horizonte
    indices_positivos = np.where(angulos_solares > 0)[0]
    
    if len(indices_positivos) > 0:
        indice_nascer = indices_positivos[0]
        indice_poente = indices_positivos[-1]
        hora_nascer = horas[indice_nascer]
        hora_poente = horas[indice_poente]
        return hora_nascer, hora_poente
    else:
        return None, None

def gerar_grafico_tamanho_da_sombra(dia, latitude, altura_objeto, remover_outliers=True):
    # Obter horários de nascer e pôr
    hora_nascer, hora_poente = obter_nascer_poente(dia, latitude)
    
    if hora_nascer is None or hora_poente is None:
        print("Aviso: Sol não nasceu neste dia (latitude muito extrema)")
        return
    
    # Gerar dados apenas no período do dia
    horas = np.linspace(hora_nascer, hora_poente, 100)
    declinacao, angulos_horarios, angulos_solares = calcular_dados_solares(dia, latitude, horas)
    sombras = tamanho_da_sombra_no_plano_horizontal(altura_objeto, angulos_solares)
    
    # Remover outliers se solicitado
    if remover_outliers:
        mascara = remover_outliers_sombra(sombras, metodo='percentil')
        horas = horas[mascara]
        angulos_horarios = angulos_horarios[mascara]
        sombras = sombras[mascara]
    
    # Converter para radianos para gráfico polar
    angulos_rad = np.radians(angulos_horarios)
    
    # Criar figura com projeção polar
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Plotar a sombra em coordenadas polares
    ax.plot(angulos_rad, sombras, 'b-', linewidth=2, label='Tamanho da Sombra')
    
    # Destacar o nascer do sol (primeiro ponto válido)
    ax.scatter([angulos_rad[0]], [sombras[0]], color='orange', s=150, 
              zorder=5, label=f'Nascer ({horas[0]:.1f}h)', marker='o')
    
    # Destacar o poente do sol
    ax.scatter([angulos_rad[-1]], [sombras[-1]], color='red', s=150, 
              zorder=5, label=f'Poente ({horas[-1]:.1f}h)', marker='o')
    
    # Configurações do gráfico polar
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('Comprimento da Sombra ao Longo do Dia')
    ax.set_ylim(0, max(sombras) * 1.1)
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    plt.show()

def __main__():
    dia = 9
    mes = 6
    latitude = -14
    altura_objeto = 1

    dia_do_ano = obter_dia_do_ano(dia, mes)
    gerar_grafico_tamanho_da_sombra(dia_do_ano, latitude, altura_objeto)

if __name__ == "__main__":
    __main__()