class VotacionTemp:
    def __init__(self, voto_id, mesa_id, ciudadano_dpi, fecha_hora):
        self.voto_id = voto_id
        self.mesa_id = mesa_id
        self.ciudadano_dpi = ciudadano_dpi
        self.fecha_hora = fecha_hora
        self.candidatos = []  # Lista para almacenar los candidatos

    def agregar_candidato(self, id_candidato):
        self.candidatos.append(id_candidato)
