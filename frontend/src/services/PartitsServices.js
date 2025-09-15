import api from '../api.js'

class PartitService {
    async create({ fase_id, jornada, equip_local_id, equip_visitant_id }){
        const response = await api.post('/partit/', {
            fase_id,
            jornada,
            equip_local_id,
            equip_visitant_id
        })

    }
     async getByJornada(fase_id, jornada) {
        const response = await api.get(`/partit/${fase_id}/jornada/${jornada}`)
        return response.data
    }

     async updateResultat(partit_id, gols_local, gols_visitant) {
        const response = await api.put(`/partit/${partit_id}/gols`, {
            gols_local,
            gols_visitant
        })
        return response.data
    }
    async getQuadreResultats(fase_id){
        const response = await api.get(`/partit/quadre/${fase_id}`)
        console.log(response.data)
        return response.data

    }

}
export default new PartitService()