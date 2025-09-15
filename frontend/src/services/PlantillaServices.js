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
}

export default new PlantillaService()