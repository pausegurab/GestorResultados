import api from '../api.js';

class CompetitionService {
  async getAll() {
    const response = await api.get('/competicio/');
    return response.data;
  }
  async getById(id) {
    const response = await api.get(`/competicio/${id}`);
    return response.data;
  }
  async createForm(data) {
    console.log('Creating competition with data:', data);
    const response = await api.post('/competicio/', data)
    return response.data
  }
  async updateForm(id, data) {
    const response = await api.put(`/competcio/${id}`, data)
    return response.data
  }
  async delete(id) {
    const response = await api.delete(`/competicio/${id}`)
    return response.data
  }
}

export default new CompetitionService();