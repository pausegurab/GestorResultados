<script setup>
import { ref, onMounted, computed } from 'vue'
import JugadorService from '../services/JugadorsServices.js'
import CountryService from '../services/CountryServices.js'

const jugadors = ref([])
const paisos = ref([])
const showModal = ref(false)
const menuOpen = ref(null)
const editMode = ref(false)
const jugadorEditant = ref(null)

const form = ref({
  nom: '',
  cognom_1: '',
  cognom_2: '',
  sobrenom: '',
  posicio: '',
  nacionalitat: null,
  url_imatge: '',
  data_naixement: ''
})

const fetchJugadors = async () => {
  jugadors.value = await JugadorService.getAll()
}
const fetchPaisos = async () => {
  paisos.value = await CountryService.getAll()
}

onMounted(() => {
  fetchJugadors()
  fetchPaisos()
})

function obrirModal() {
  form.value = {
    nom: '',
    cognom_1: '',
    cognom_2: '',
    sobrenom: '',
    posicio: '',
    nacionalitat: null,
    url_imatge: '',
    data_naixement: ''
  }
  editMode.value = false
  jugadorEditant.value = null
  showModal.value = true
}

function tancarModal() {
  showModal.value = false
  editMode.value = false
  jugadorEditant.value = null
}

function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}

function obrirEditarJugador(jugador) {
  jugadorEditant.value = jugador.id
  editMode.value = true
  form.value = {
    nom: jugador.nom,
    cognom_1: jugador.cognom_1,
    cognom_2: jugador.cognom_2,
    sobrenom: jugador.sobrenom,
    posicio: jugador.posicio,
    nacionalitat: jugador.nacionalitat,
    url_imatge: jugador.url_imatge,
    data_naixement: jugador.data_naixement?.split('T')[0] || ''
  }
  showModal.value = true
  menuOpen.value = null
}

async function crearJugador() {
  const {
    nom,
    cognom_1,
    cognom_2,
    sobrenom,
    posicio,
    nacionalitat,
    url_imatge,
    data_naixement
  } = form.value

  if (!nom || !cognom_1 || !posicio || isNaN(parseInt(nacionalitat))) {
    alert('Cal omplir tots els camps obligatoris!')
    return
  }

  try {
    await JugadorService.create({
      nom,
      cognom_1,
      cognom_2,
      sobrenom,
      posicio,
      nacionalitat: parseInt(nacionalitat),
      url_imatge,
      data_naixement
    })
    await fetchJugadors()
    showModal.value = false
  } catch (e) {
    alert('Error creant el jugador')
    console.error(e)
  }
}

async function editarJugador() {
  try {
    await JugadorService.update(jugadorEditant.value, {
      ...form.value,
      nacionalitat: parseInt(form.value.nacionalitat)
    })
    await fetchJugadors()
    tancarModal()
  } catch (e) {
    alert('Error editant el jugador')
    console.error(e)
  }
}

async function eliminarJugador(id) {
  if (confirm('Segur que vols esborrar aquest jugador?')) {
    try {
      await JugadorService.delete(id)
      await fetchJugadors()
      menuOpen.value = null
    } catch (e) {
      alert('Error esborrant el jugador')
      console.error(e)
    }
  }
}

async function enviarFormulari() {
  if (editMode.value) {
    await editarJugador()
  } else {
    await crearJugador()
  }
}

const sort = ref({ by: 'cognom_1', dir: 'asc' })

function ordenarPer(camp) {
  if (sort.value.by === camp) {
    sort.value.dir = sort.value.dir === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value.by = camp
    sort.value.dir = 'asc'
  }
}

const jugadorsOrdenats = computed(() => {
  const ordenats = [...jugadors.value]

  ordenats.sort((a, b) => {
    let valA, valB

    if (sort.value.by === 'posicio') {
      const ordrePosicions = ['POR', 'DEF', 'MIG', 'DAV']
      valA = ordrePosicions.indexOf(a.posicio)
      valB = ordrePosicions.indexOf(b.posicio)
    } else if (sort.value.by === 'nacionalitat') {
      const nomPais = id =>
        paisos.value.find(p => p.id === id)?.nom || ''
      valA = nomPais(a.nacionalitat)
      valB = nomPais(b.nacionalitat)
    } else if (sort.value.by === 'sobrenom') {
      valA = a.sobrenom || a.cognom_1
      valB = b.sobrenom || b.cognom_1
    } else {
      valA = a[sort.value.by]
      valB = b[sort.value.by]
    }

    if (typeof valA === 'string' && typeof valB === 'string') {
      return sort.value.dir === 'asc'
        ? valA.localeCompare(valB)
        : valB.localeCompare(valA)
    }

    return sort.value.dir === 'asc' ? valA - valB : valB - valA
  })

  return ordenats
}
)
const filtre = ref('')

const jugadorsFiltrats = computed(() =>
  jugadorsOrdenats.value.filter(j =>
    (j.sobrenom || `${j.nom} ${j.cognom_1}` || '')
      .toLowerCase()
      .includes(filtre.value.toLowerCase())
  )
)
</script>

<template>
  <div class="main-container">
    <header class="header">
      <h2>Jugadors</h2>
      <div style="display: flex; gap: 1rem; align-items: center;">
        <input
          v-model="filtre"
          type="text"
          placeholder="Cerca jugador..."
          style="padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #ccc;"
        />
        <button class="crear-btn" @click="obrirModal">Crear jugador</button>
      </div>
    </header>

    <table class="table align-middle">
      <thead>
        <tr>
          <th>Foto</th>
          <th @click="ordenarPer('sobrenom')" style="cursor:pointer;">
            Nom complet
            <span v-if="sort.by === 'sobrenom'">{{ sort.dir === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="ordenarPer('posicio')" style="cursor:pointer;">
            Posició
            <span v-if="sort.by === 'posicio'">{{ sort.dir === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="ordenarPer('nacionalitat')" style="cursor:pointer;">
            País
            <span v-if="sort.by === 'nacionalitat'">{{ sort.dir === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="j in jugadorsFiltrats" :key="j.id">
          <td>
            <img v-if="j.url_imatge" :src="j.url_imatge" alt="Foto jugador" style="max-width:80px; max-height:80px; border-radius:12px;">
          </td>
          <td>{{ j.sobrenom || `${j.nom} ${j.cognom_1}` }}</td>
          <td>{{ j.posicio }}</td>
          <td>
            <img
              v-if="paisos.find(p => p.id === j.nacionalitat)?.url_imatge"
              :src="paisos.find(p => p.id === j.nacionalitat).url_imatge"
              :alt="paisos.find(p => p.id === j.nacionalitat)?.nom"
              style="max-width:40px; max-height:40px; border-radius:8px; background:#fff;"
            />
          </td>
          <td style="position: relative;">
            <button class="menu-btn" @click="toggleMenu(j.id)">&#8942;</button>
            <div v-if="menuOpen === j.id" class="menu-dropdown">
              <div @click="obrirEditarJugador(j)">Editar jugador</div>
              <div @click="eliminarJugador(j.id)">Esborrar jugador</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModal" class="modal-overlay" @click.self="tancarModal">
      <div class="modal">
        <h3>{{ editMode ? 'Editar jugador' : 'Nou jugador' }}</h3>
        <form @submit.prevent="enviarFormulari">
          <label>
            Nom:
            <input v-model="form.nom" required />
          </label>
          <label>
            Primer cognom:
            <input v-model="form.cognom_1" required />
          </label>
          <label>
            Segon cognom:
            <input v-model="form.cognom_2" />
          </label>
          <label>
            Sobrenom:
            <input v-model="form.sobrenom" />
          </label>
          <label>
            Posició:
            <select v-model="form.posicio" required>
              <option disabled value="">Selecciona una posició</option>
              <option value="POR">Porter</option>
              <option value="DEF">Defensa</option>
              <option value="MIG">Migcampista</option>
              <option value="DAV">Davanter</option>
            </select>
          </label>
          <label>
            Nacionalitat:
            <select v-model="form.nacionalitat" required>
              <option disabled value="">Selecciona un país</option>
              <option v-for="pais in paisos" :key="pais.id" :value="pais.id">
                {{ pais.nom }}
              </option>
            </select>
          </label>
          <div v-if="form.nacionalitat">
            <img
              v-if="paisos.find(p => p.id === form.nacionalitat)?.url_imatge"
              :src="paisos.find(p => p.id === form.nacionalitat).url_imatge"
              alt="Imatge país"
              style="max-width: 40px; max-height: 40px; margin-top: 0.5rem;"
            />
          </div>
          <label>
            Imatge (URL):
            <input v-model="form.url_imatge" type="text" placeholder="https://..." />
          </label>
          <label>
            Data de naixement:
            <input v-model="form.data_naixement" type="date" />
          </label>
          <div class="modal-actions">
            <button type="button" @click="tancarModal">Cancel·la</button>
            <button type="submit">{{ editMode ? 'Desa' : 'Crea' }}</button>
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
.table {
  width: 100%;
  margin-top: 2rem;
  border-collapse: collapse;
  background: #fff;
}
.table th, .table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.table th {
  background: #111;
  color: #fff;
}
.table tr:last-child td {
  border-bottom: none;
}

.competicio-nom {
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  word-break: break-word;
  width: 100%;
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
.menu-btn {
  background: none;
  border: none;
  color: #000000 !important;
  font-size: 1.5rem;
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #222;
  padding: 2rem;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
.modal h3 {
  margin-top: 0;
  color: #fff;
}
.modal label {
  display: block;
  margin-bottom: 0.5rem;
  color: #ddd;
}
.modal input, .modal select {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 4px;
}
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.modal-actions button {
  flex: 1 1 0;
  padding: 0.75rem 0;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  transition: background 0.2s;
}
.modal-actions button[type="button"] {
  background-color: #e53935;
}
.modal-actions button[type="button"]:hover {
  background-color: #b71c1c;
}
.modal-actions button[type="submit"] {
  background-color: #1976d2;
}
.modal-actions button[type="submit"]:hover {
  background-color: #1565c0;
}
</style>
