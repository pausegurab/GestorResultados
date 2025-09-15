<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TemporadaService from '../services/TemporadesServices.js'

const temporades = ref([])
const route = useRoute()
const router = useRouter()
const showModal = ref(false)
const form = ref({
  any_inici: '',
  any_fi: '',
  numero_equips: null
})
const menuOpen = ref(null)
const showFaseModal = ref(false)
const faseForm = ref({
  nom: '',
  tipus: 'lliga'
})
let temporadaIdCreada = null

const fetchTemporades = async () => {
  const competicio_id = route.query.competicio
  console.log('Fetching temporades for competicio:', competicio_id)
  if (competicio_id) {
    temporades.value = await TemporadaService.getByCompeticio(competicio_id)
    console.log('Fetched temporades:', temporades.value)
  }
}

onMounted(() => {
  fetchTemporades()
})

function obrirModal() {
  form.value = { any_inici: '', any_fi: '', numero_equips: '' }
  showModal.value = true
}

function tancarModal() {
  showModal.value = false
}
function anarAVistaCompeticio(temporadaId) {
  router.push({ path: '/vistaCompeticio', query: { temporada: temporadaId } })
}

async function crearTemporada() {
  const competicio_id = parseInt(route.query.competicio)
  const any_inici = parseInt(form.value.any_inici)
  const any_fi = parseInt(form.value.any_fi)
  const numero_equips = parseInt(form.value.numero_equips)

  if (!any_inici || !any_fi || !numero_equips) {
    alert('Cal omplir tots els camps!')
    return
  }
  try {
    const resposta = await TemporadaService.create({
      competicio_id,
      any_inici,
      any_fi,
      numero_equips
    })
    await fetchTemporades()
    showModal.value = false

    temporadaIdCreada = resposta.id
    showFaseModal.value = true
    faseForm.value = { nom: '', tipus: 'lliga' }
  } catch (e) {
    alert('Error creant la temporada')
    console.error(e)
  }
}

async function crearFase() {
  if (!faseForm.value.nom) {
    alert('Cal posar un nom de fase!')
    return
  }
  console.log('Creating fase with form:', faseForm.value.tipus)
  try {
    await TemporadaService.createFase({
      nom: faseForm.value.nom,
      tipus: faseForm.value.tipus,
      ordre: 1,
      temporada_id: temporadaIdCreada
    })
    showFaseModal.value = false
    await fetchTemporades()
  } catch (e) {
    alert('Error creant la fase')
    console.error(e)
  }
}

function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}
 
async function esborrarTemporada(id) {
  const t = temporades.value.find(x => x.id === id)
  if (!t) return
  const confirmat = confirm(`Segur que vols esborrar la temporada ${t.any_inici} - ${t.any_fi}?`)
  if (!confirmat) return

  try {
    await TemporadaService.delete(id)
    await fetchTemporades()
  } catch (e) {
    alert('Error esborrant la temporada')
    console.error(e)
  }
}

const temporadesOrdenades = computed(() =>
  [...temporades.value].sort((a, b) => a.any_inici - b.any_inici)
)
</script>

<template>
  <div class="main-container">
    <header class="header">
      <h2>Temporades</h2>
      <button class="crear-btn" @click="obrirModal">Crear temporada</button>
    </header>
    <div class="cards-container">
      <div v-for="t in temporadesOrdenades" :key="t.id" class="competicio-card">
        <div class="card-left">
          <span class="competicio-nom clicable" @click="anarAVistaCompeticio(t.id)">
            {{ t.any_inici }} - {{ t.any_fi }}
          </span>
        </div>
        <div class="card-menu">
          <button class="menu-btn" @click="toggleMenu(t.id)">&#8942;</button>
          <div v-if="menuOpen === t.id" class="menu-dropdown">
            <div @click="esborrarTemporada(t.id)">Esborrar temporada</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="tancarModal">
      <div class="modal">
        <h3>Nova temporada</h3>
        <form @submit.prevent="crearTemporada">
          <label>
            Any inici:
            <input v-model="form.any_inici" type="number" required min="1900" max="2100" />
          </label>
          <label>
            Any fi:
            <input v-model="form.any_fi" type="number" required min="1900" max="2100" />
          </label>
          <label>
            Número d'equips:
            <input v-model="form.numero_equips" type="number" required min="2" max="100" />
          </label>
          <div class="modal-actions">
            <button type="button" @click="tancarModal">Cancel·la</button>
            <button type="submit">Crea</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showFaseModal" class="modal-overlay" @click.self="showFaseModal = false">
      <div class="modal">
        <h3>Nova fase</h3>
        <form @submit.prevent="crearFase">
          <label>
            Nom de la fase:
            <input v-model="faseForm.nom" required />
          </label>
          <label>
            Tipus:
            <select v-model="faseForm.tipus" required>
              <option value="lliga">Lliga</option>
              <option value="eliminatoria">Eliminatòria</option>
            </select>
          </label>
          <div class="modal-actions">
            <button type="button" @click="showFaseModal = false">Cancel·la</button>
            <button type="submit">Crea fase</button>
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
.cards-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
  margin-top: 2rem;
}
.competicio-card {
  aspect-ratio: 1 / 1;
  width: 100%;
  max-width: 220px;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #111;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  position: relative;
  margin: 0 auto;
}
.card-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
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
.modal button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  width: 48%;
  margin-right: 4%;
}
.modal button:last-child {
  margin-right: 0;
  background-color: #e53935;
}
.modal button:hover {
  background-color: #1565c0;
}
.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
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
.clicable {
  transition: color 0.2s;
}
.clicable:hover {
  text-decoration: underline;
  cursor: pointer;
}

</style>