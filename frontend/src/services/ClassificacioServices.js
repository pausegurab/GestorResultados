import api from '../api.js';

class ClassificacioService {
    async createPrimeraJornada({fase_id, equip_id}){
        console.log('Creating first matchday classification for fase_id:', fase_id, 'and equip_id:', equip_id);
        const response = await api.post(`/classificacio/primera_jornada?fase_id=${fase_id}&equip_id=${equip_id}`);
        return response.data;
    }
    async getClassificacioByJornada(fase_id, jornada) {
        const response = await api.get(`/classificacio/${fase_id}/${jornada}`);
        return response.data;
    }
    async getClassificacioHistoric(fase_id) {
        const response = await api.get(`/classificacio/historic/${fase_id}`);
        return response.data;
    }

}

export default new ClassificacioService();