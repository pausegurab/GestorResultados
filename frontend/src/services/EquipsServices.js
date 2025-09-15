import api from '../api.js'

class EquipService {
    async getAll() {
        const response = await api.get('/equips/')
        return response.data
    }

    async getById(id) {
        const response = await api.get(`/equips/${id}`)
        return response.data
    }

    async create({ nom, sigles, foto, pais_id }) {  
        console.log('Creating equip:', { nom, sigles, foto, pais_id })
        const response = await api.post('/equips/', {
            nom: nom,
            sigles: sigles,
            foto: foto,
            pais_id: parseInt(pais_id)
        })
        return response.data  
    }
    async delete(id) {
        const response = await api.delete(`/equips/${id}`)
        return response.data
    }
}
 export default new EquipService()