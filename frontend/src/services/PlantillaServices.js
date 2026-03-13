import api from '../api.js'

class PlantillaService {
  async getByEquipITemporada(equip_id, temporada_id) {
    const res = await api.get(`/plantilla/${equip_id}/${temporada_id}`)
    return res.data
  }

  async crearPlantilla(equip_id, temporada_id, jugador_ids) {
    const res = await api.post('/plantilla/', {
      equip_id,
      temporada_id,
      jugador_ids
    })
    return res.data
  }

  async assignarDorsal(jugador_equip_temporada_id, dorsal, dorsal_start_jornada, dorsal_end_jornada = null) {
    console.log('Assignant dorsal:', {jugador_equip_temporada_id, dorsal, dorsal_start_jornada, dorsal_end_jornada})
    const res = await api.put(`/plantilla/${jugador_equip_temporada_id}/dorsal`, {
      dorsal,
      dorsal_start_jornada,
      dorsal_end_jornada
    })
    return res.data
  }
  async clonarPlantilla(equip_id, temporada_id, destino_temporada_id){
    console.log("Clonant plantilla...")
    const res = await api.post(`/plantilla/clone`, {
      equip_id,
      temporada_id,
      destino_temporada_id
    })
    return res.data
  }
}

export default new PlantillaService()