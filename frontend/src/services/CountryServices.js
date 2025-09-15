import api from '../api.js'

class CountryService {
  async getAll() {
    const response = await api.get('/paissos/')
    return response.data
  }
  async getById(id) {
    const response = await api.get(`/paissos/${id}`)
    return response.data
  }
}

export default new CountryService()