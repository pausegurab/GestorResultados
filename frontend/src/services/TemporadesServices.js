import api from '../api.js'

class TemporadaService {
  async getAll() {
    const response = await api.get('/temporada/')
    return response.data
  }
  async getByCompeticio(competicio_id) {
    console.log('Fetching temporades for competicio:', competicio_id)
    const response = await api.get(`/temporada/competicio/${competicio_id}`)
    return response.data
  }
  async getById(temporada_id) {
    const response = await api.get(`/temporada/${temporada_id}`)
    return response.data
  }
  async create({competicio_id, any_inici, any_fi, numero_equips}) {
    console.log('Creating temporada:', {competicio_id, any_inici, any_fi, numero_equips})
    const response = await api.post('/temporada/', {
      competicio_id: parseInt(competicio_id),
      any_inici: any_inici,
      any_fi: any_fi,
      numero_equips: numero_equips  
    })
    return response.data  
  }
  async delete(id){
    console.log('Deleting temporada with id:', id)
    const response = await api.delete(`/temporada/${id}`)
    return response.data
  }
  async createFase(fase) {
    const response = await api.post('/fases/', fase)
    return response.data
  }
}
export default new TemporadaService()