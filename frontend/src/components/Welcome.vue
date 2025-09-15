<script setup>
import { ref, onMounted } from 'vue'
import CompetitionService from '../services/CompetitionServices.js'
import CountryService from '../services/CountryServices.js'
import { useRouter } from 'vue-router'

const router = useRouter()

const competicions = ref([])
const paisos = ref([])
const menuOpen = ref(null)
const showModal = ref(false)

const editData = ref({
  id: null,
  nom: '',
  tipus: '',
  foto: '',
  pais_id: null
})

const tipusOptions = [
  { value: 'lliga', label: 'Lliga' },
  { value: 'copa', label: 'Copa' },
  { value: 'mixte', label: 'Mixte' }
]

const fetchCompeticions = async () => {
  competicions.value = await CompetitionService.getAll()
}

const fetchPaisos = async () => {
  paisos.value = await CountryService.getAll()
}

onMounted(() => {
  fetchCompeticions()
  fetchPaisos()
})

function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}

function editarCompeticio(id) {
  const c = competicions.value.find(x => x.id === id)
  if (!c) return
  editData.value = {
    id: c.id,
    nom: c.nom,
    tipus: c.tipus,
    foto: c.foto || '',
    pais_id: c.pais_id
  }
  showModal.value = true
  menuOpen.value = null
}

function obrirCrear() {
  editData.value = {
    id: null,
    nom: '',
    tipus: '',
    foto: '',
    pais_id: null
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveEdit() {
  const data = {
    nom: editData.value.nom,
    tipus: editData.value.tipus,
    foto: editData.value.foto || null, // backend espera Optional[str]
    pais_id: editData.value.pais_id ? parseInt(editData.value.pais_id) : null
  }

  if (!data.pais_id) {
    alert('Has de seleccionar un país!')
    return
  }

  try {
    if (editData.value.id) {
      await CompetitionService.updateForm(editData.value.id, data)
    } else {
      await CompetitionService.createForm(data)
    }
    await fetchCompeticions()
    showModal.value = false
  } catch (e) {
    console.error(e)
    alert('Error al desar la competició')
  }
}

async function esborrarCompeticio(id) {
  const c = competicions.value.find(x => x.id === id)
  if (!c) return
  const confirmat = confirm(`Segur que vols esborrar la competició "${c.nom}"?`)
  if (!confirmat) return

  try {
    await CompetitionService.delete(id)
    await fetchCompeticions()
  } catch (e) {
    alert('Error esborrant la competició')
    console.error(e)
  }
}

function getPaisById(id) {
  return paisos.value.find(pais => pais.id === id)
}
</script>

<template>
  <div class="main-container">
    <header class="header">
      <h2>Competicions</h2>
      <button class="crear-btn" @click="obrirCrear">Crear competició</button>
    </header>
    <div class="cards-container">
      <div v-for="c in competicions" :key="c.id" class="competicio-card">
        <div class="card-left">
          <span
            class="competicio-nom"
            @click="router.push({ path: '/temporades', query: { competicio: c.id } })"
          >
            {{ c.nom }}
          </span>
          <img
            v-if="getPaisById(c.pais_id)?.url_imatge"
            :src="getPaisById(c.pais_id).url_imatge"
            alt="Bandera país"
            style="width: 32px; height: 32px; margin-left: 1rem; border-radius: 4px; background: #fff;"
          />
        </div>
        <div class="card-right" v-if="c.foto">
  <img :src="c.foto" alt="Imatge competició" />
</div>
        <div class="card-menu">
          <button class="menu-btn" @click="toggleMenu(c.id)">&#8942;</button>
          <div v-if="menuOpen === c.id" class="menu-dropdown">
            <div @click="editarCompeticio(c.id)">Editar competició</div>
            <div @click="esborrarCompeticio(c.id)">Esborrar competició</div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>Edita competició</h3>
        <form @submit.prevent="saveEdit">
          <label>
            Nom:
            <input v-model="editData.nom" required />
          </label>
          <label>
            Tipus:
            <select v-model="editData.tipus" required>
              <option v-for="opt in tipusOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </label>
          <label>
            País:
            <select v-model="editData.pais_id" required>
              <option disabled value="">Selecciona un país</option>
              <option v-for="pais in paisos" :key="pais.id" :value="pais.id">
                {{ pais.nom }}
              </option>
            </select>
          </label>
          <div v-if="editData.pais_id">
            <img
              v-if="paisos.find(p => p.id === editData.pais_id)?.url_imatge"
              :src="paisos.find(p => p.id === editData.pais_id).url_imatge"
              alt="Imatge país"
              style="max-width: 40px; max-height: 40px; margin-top: 0.5rem;"
            />
          </div>
          <label>
            Imatge (URL):
            <input v-model="editData.foto" type="text" placeholder="https://..." />
          </label>
          <div class="modal-actions">
            <button type="button" @click="closeModal">Cancel·la</button>
            <button type="submit">Desa</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  padding-left: 2rem;
  padding-right: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.crear-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.2rem;
}

.crear-btn:hover {
  background-color: #1565c0;
}

.cards-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

.competicio-card {
  display: flex;
  background: #111;
  border-radius: 12px;
  overflow: visible;
  min-height: 120px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  position: relative;
}

.card-left {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 2rem;
}

.competicio-nom {
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  cursor: pointer;
  transition: text-decoration 0.2s;
}

.competicio-nom:hover {
  text-decoration: underline;
  cursor: pointer;
}

.card-right {
  width: 40%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #222;
}

.card-right img {
  max-width: 100%;
  max-height: 100px;
  object-fit: contain;
  border-radius: 0 12px 12px 0;
}

.card-menu {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.menu-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.menu-dropdown {
  position: absolute;
  right: 0;
  margin-top: 0.5rem;
  background: #222;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  z-index: 10;
  min-width: 180px;
  overflow: hidden;
}

.menu-dropdown div {
  color: #fff;
  padding: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.menu-dropdown div:hover {
  background: #333;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #222;
  color: #fff;
  padding: 2rem;
  border-radius: 12px;
  min-width: 320px;
  max-width: 90vw;
  box-shadow: 0 2px 16px rgba(0,0,0,0.4);
}
.modal label {
  display: block;
  margin: 1rem 0 0.5rem 0;
}
.modal input, .modal select {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  border: none;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
.modal-actions button {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  border: none;
  font-weight: bold;
  cursor: pointer;
}
.modal-actions button[type="submit"] {
  background: #1976d2;
  color: #fff;
}
.modal-actions button[type="button"] {
  background: #444;
  color: #fff;
}
</style>
