import api from '../api.js'

class JugadorService {
    async getAll() {
        const response = await api.get('/jugadors/')
        return response.data
    }

    async getById(id) {
        const response = await api.get(`/jugadors/${id}`)
        return response.data
    }

    async create({nom, cognom_1, cognom_2, sobrenom, posicio, nacionalitat, url_imatge, data_naixement }) {
        console.log("Creating jugador with data:", {
            nom,
            cognom_1,
            cognom_2,
            sobrenom,
            posicio,
            nacionalitat,
            url_imatge,
            data_naixement
        })
        const response = await api.post('/jugadors/', {
            nom: nom,
            cognom_1: cognom_1,
            cognom_2: cognom_2,
            sobrenom: sobrenom,
            posicio: posicio,
            nacionalitat: nacionalitat,
            url_imatge: url_imatge,
            data_naixement: data_naixement
        })
        return response.data
    }
    async update(id, jugador) {
        const res = await api.put(`jugadors/${id}`, jugador)
        return res.data
    }

    async delete(id) {
        const response = await api.delete(`/jugadors/${id}`)
        return response.data
    }
}
export default new JugadorService()