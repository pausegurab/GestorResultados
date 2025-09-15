import api from '../api.js'


class ParticipationService {
    
    async create({temporada_id, equip_id }) {
        const response = await api.post('/participacio/', {
            temporada_id: parseInt(temporada_id),
            equip_id: parseInt(equip_id)
        })
        return response.data
    }
    async getByTemporada(temporada_id) {
        const response = await api.get(`/participacio/${temporada_id}/equips`)
        return response.data
    }
    async delete(equip_id, temporada_id) {
        const response = await api.delete(`/participacio/${temporada_id}/equips/${equip_id}`)
        return response.data
    }
    async getFasesLligaByTemporada(temporada_id) {
        const response = await api.get(`/fases/lliga/${temporada_id}`)
        return response.data
    }  
}

export default new ParticipationService()