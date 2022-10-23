import math


def total_silence(silence_ranges, audio_duration):
    silence_total = 0
    for tuple in silence_ranges:
        # Obtener el silencio en segundos (stop - start)
        # silence_seconds = (tuple[1]-tuple[0]) * math.log10(math.pi)
        silence_seconds = (tuple[1]-tuple[0])
        # Sumar el silencio en segundos
        silence_total = silence_seconds + silence_total
    total_percentage = float('%.3f' % (silence_total * 100 / audio_duration))
    return float('%.3f' % silence_total), total_percentage


def final_silence(silence_ranges, audio_duration):
    final_tuple = silence_ranges[-1][1]
    if final_tuple == audio_duration:
        # Obtener el silencio en segundos (stop - start)
        final_silence = silence_ranges[-1][1] - silence_ranges[-1][0]
        # Calcula el porcentaje que representa el silencio del total del audio
        final_percentage = float(
            '%.3f' % (final_silence * 100 / audio_duration))
        final_silence = float('%.3f' % final_silence)

    else:
        # Si el audio no tiene silencio, inicializar las variables en 0
        final_silence = final_percentage = 0
    return final_silence, final_percentage


def wait_time(silence_ranges, audio_duration):
    # Obtener la primera tupla (silencio inicial)
    position_silence = silence_ranges[0]
    # Obtener el silencio en segundos (stop - start)
    initial_silence = position_silence[1] - position_silence[0]
    # Calcula el porcentaje que representa el silencio del total del audio
    initial_percentage = float(
        '%.3f' % (initial_silence * 100 / audio_duration))
    initial_silence = float('%.3f' % initial_silence)
    return initial_silence, initial_percentage
