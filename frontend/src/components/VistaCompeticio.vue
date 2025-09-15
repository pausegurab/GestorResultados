<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TemporadaService from '../services/TemporadesServices.js'
import CompetitionService from '../services/CompetitionServices.js'
import EquipService from '../services/EquipsServices.js'
import ParticipationServices from '../services/ParticipationServices.js'
import ClassificacioServices from '../services/ClassificacioServices.js'
import PartitsServices from '../services/PartitsServices.js'

const competicio = ref(null)
const temporada = ref(null)
const equips = ref([])
const equipsATemporada = ref([])
const partits = ref ([])
const quadreEquips   = ref([])       
const quadreResultat = ref([]) 


const showModal = ref(false)
const menuOpen = ref(null)
const showModalPartits = ref(false)
const editMode = ref(false)

const fase = ref([])
const jornadaMaxima = ref(null)
const classificacio = ref([])
const jornadaActual = ref(1)
const historicChart = ref(null)


const equipsOrdenats = computed(() =>
  [...equipsATemporada.value].sort((a, b) => a.nom.localeCompare(b.nom))
)

const form = ref({ equip_id: '' })

const formPartits = ref({equipLocal: '', equipVisitant: '', jornada: ''})

const tabs = ['Equips', 'Classificació', 'Partits', 'Quadre', 'Històric']
const activeTab = ref('Equips')

const route = useRoute()
const router = useRouter()

function veureDetall(id) {
  router.push({
    name: 'equip-detall',
    params: { id },
    query: { competicio_id: competicio.value.id }
  })
}

function getNomEquip(equip_id) {
  const equip = equipsATemporada.value.find(e => e.id === equip_id)
  return equip ? equip.nom : 'Equip desconegut'
}

function getEquipById(id) {
  return equipsATemporada.value.find(e => e.id === id) || { nom: 'Desconegut', foto: '' }
}

async function fetchDades () {
  const temporadaId = route.query.temporada
  if (!temporadaId) return

  temporada.value = await TemporadaService.getById(temporadaId)
  competicio.value = await CompetitionService.getById(temporada.value.competicio_id)
  fase.value = await ParticipationServices.getFasesLligaByTemporada(temporadaId)
}
function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}
async function fetchEquips () {
  equips.value = await EquipService.getAll()
}

onMounted(async () => {
  await fetchDades()
  await fetchEquips()
  await fetchEquipsATemporada()
  await fetchClassificacio()
  await fetchPartits()
  await fetchQuadre()
  


  const numEquips = equipsATemporada.value.length
  jornadaMaxima.value = (numEquips - 1) * 2
  jornadaActual.value = jornadaMaxima.value
  
})

function obrirModal () {
  form.value.equip_id = ''
  showModal.value = true
}

function obrirModalPartits () {
  showModalPartits.value = true
}
function tancarModal () {
  showModal.value = false
}

function tancarModalPartit() {
  showModalPartits.value = false
}
async function fetchClassificacio () {
  const fase_id = fase.value[0].id
  console.log(fase_id)
  if (!fase_id) return
  try {
    const data = await ClassificacioServices.getClassificacioByJornada(fase_id, jornadaActual.value)
    classificacio.value = data
  } catch (err) {
    console.error('Error carregant classificació:', err)
    classificacio.value = []
  }
}

async function fetchPartits () {
  const fase_id = fase.value[0]?.id
  if (!fase_id) return
  try {
    partits.value = await PartitsServices.getByJornada(fase_id, jornadaActual.value)
  } catch (err) {
    console.error('Error carregant partits:', err)
    partits.value = []
  }
}


function anteriorJornada () {
  if (jornadaActual.value > 1) {
    jornadaActual.value--
    fetchClassificacio()
  }
}
function seguentJornada () {
  jornadaActual.value++
  fetchClassificacio()
}

watch(jornadaActual, () => {
  fetchClassificacio()
  fetchPartits()
})
watch(activeTab, (novaPestanya) => {
  if (novaPestanya === 'Històric') {
    setTimeout(renderHistoricChart, 100)
  }
})

async function fetchEquipsATemporada () {
  if (!temporada.value) return
  equipsATemporada.value = await ParticipationServices.getByTemporada(temporada.value.id)
}

async function esborraEquipDeTemporada (equipId) {
  if (!temporada.value) return
  if (!confirm('Segur que vols esborrar aquest equip de la temporada?')) return

  try {
    await ParticipationServices.delete(equipId, temporada.value.id)
    await fetchEquipsATemporada()
    await fetchClassificacio()
    alert('Equip esborrat correctament!')
  } catch (err) {
    console.error(err)
    alert('Error en esborrar l\'equip')
  }
  
}
async function vincularEquipsATemporada () {
  const equip_id = parseInt(form.value.equip_id)
  const temporada_id = parseInt(temporada.value.id)
  const fase_id = fase.value[0].id
  if (!equip_id) return alert('Tria un equip')
  try {
    await ParticipationServices.create({ temporada_id, equip_id })
    await ClassificacioServices.createPrimeraJornada({fase_id, equip_id})
    await fetchDades()
    await fetchEquipsATemporada()
    const numEquips = equipsATemporada.value.length
    jornadaMaxima.value = (numEquips - 1) * 2

    await fetchClassificacio()
    tancarModal()
    
    alert('Equip vinculat correctament!')
  } catch (err) {
    console.error(err)
    alert('Error en vincular l\'equip')
  }
}

async function crearPartit () {
  const { equipLocal, equipVisitant, jornada } = formPartits.value
  const fase_id = fase.value[0].id

  if (!equipLocal || !equipVisitant || !jornada) {
    alert('Omple tots els camps!')
    return
  }
  if (equipLocal === equipVisitant) {
    alert('Local i visitant no poden ser el mateix equip')
    return
  }

  try {
    await PartitsServices.create({
      fase_id,
      jornada: parseInt(jornada),
      equip_local_id: parseInt(equipLocal),
      equip_visitant_id: parseInt(equipVisitant)
    })
    alert('Partit creat correctament')
    showModalPartits.value = false
    await fetchPartits()
  } catch (err) {
    console.error(err)
    alert('Error en crear el partit')
  }
}
async function fetchQuadre () {
   const fase_id = fase.value[0].id
  if (!fase_id) return
  try {
    const data = await PartitsServices.getQuadreResultats(fase_id)
    quadreEquips.value   = data.equips
    console.log(quadreEquips.value)
    quadreResultat.value = data.resultats
  } catch (err) {
    console.error('Error carregant quadre:', err)
    quadreEquips.value = []
    quadreResultat.value = []
  }
}


function onInputGols(partit) {
  const { gols_local, gols_visitant } = partit
  if (Number.isInteger(gols_local) && Number.isInteger(gols_visitant)) {
    actualitzarGols(partit)
  }
}

async function actualitzarGols(partit) {
   const { id, gols_local, gols_visitant } = partit
   const updated = await PartitsServices.updateResultat(id, gols_local, gols_visitant)
   await fetchClassificacio()
   await fetchQuadre()
  
}

async function renderHistoricChart() {
  const resposta = await ClassificacioServices.getClassificacioHistoric(fase.value[0].id)

  const jornades = resposta.jornades
  const equipsHistoric = resposta.equips

  const datasets = Object.entries(equipsHistoric).map(([nom, posicions], i) => ({
    label: nom,
    data: posicions,
    borderColor: getColor(i),
    fill: false,
    tension: 0.3,
    pointRadius: 4,
    pointHoverRadius: 6,
  }))

  if (historicChart.value) {
    historicChart.value.destroy()
  }

  const ctx = document.getElementById('historicChart').getContext('2d')
  historicChart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: jornades,
      datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          reverse: true,
          stepSize: 1,
          title: {
            display: true,
            text: 'Posició'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Jornada'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Evolució de la classificació',
          font: { size: 18 }
        },
        legend: { position: 'bottom' }
      }
    }
  })
}

function getColor(index) {
  const colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0']
  return colors[index % colors.length]
}


</script>

<template>
  <div class="main-container">
    <header class="header">
      <div class="header-left" v-if="competicio && temporada">
        <img :src="competicio.foto" alt="Logo competició" class="logo" />
        <h2>{{ competicio.nom }} {{ temporada.any_inici }}-{{ temporada.any_fi }}</h2>
      </div>
       <div class="header-buttons">
        <button class="crear-btn" @click="obrirModalPartits">Crear jornades</button>
        <button class="crear-btn" @click="obrirModal">Vincular equips</button>
      </div>
    </header>

    <nav class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab"
        :class="['tab-btn', { active: activeTab === tab }]"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </nav>

    <section v-if="activeTab === 'Equips'">
      <div v-if="activeTab === 'Equips'" class="equips-grid">
        <div v-for="equip in equipsOrdenats" :key="equip.id" @click="veureDetall(equip.id)" class="equip-card">
          <div class="card-header">
            <button class="menu-btn" @click="toggleMenu(equip.id)">⋮</button>
            <div v-if="menuOpen === equip.id" class="dropdown-menu">
              <button @click="esborraEquipDeTemporada(equip.id)">Esborra</button>
            </div>
          </div>
          <img :src="equip.foto" alt="Escut equip" class="equip-logo-top" />
          <span class="equip-nom">{{ equip.nom }}</span>
        </div>
      </div>
    </section>

    <section v-else-if="activeTab === 'Classificació'">
      <div class="classificacio-controls">
        <button @click="anteriorJornada" :disabled="jornadaActual === 1">← Jornada anterior</button>
        <span class="jornada-title">Jornada {{ jornadaActual }}</span>
        <button @click="seguentJornada" :disabled="jornadaActual === jornadaMaxima">Jornada següent →</button>
      </div>

      <table class="classificacio-taula" v-if="classificacio.length">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th>Equip</th>
          <th>PJ</th>
          <th>PG</th>
          <th>PE</th>
          <th>PP</th>
          <th>GF</th>
          <th>GC</th>
          <th>DG</th>
          <th>Punts</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(fila, index) in classificacio" :key="fila.id">
          <td>{{ index + 1 }}</td>
          <td>
            <img v-if="equipsATemporada.find(e => e.id === fila.equip_id)?.foto" 
                 :src="equipsATemporada.find(e => e.id === fila.equip_id).foto" 
                 class="equip-logo" />
                 </td>
          <td>{{ getNomEquip(fila.equip_id) }}</td>
          
          <td>{{ fila.partits_guanyats + fila.partits_empats + fila.partits_perduts }}</td>
          <td>{{ fila.partits_guanyats }}</td>
          <td>{{ fila.partits_empats }}</td>
          <td>{{ fila.partits_perduts }}</td>
          <td>{{ fila.gols_favor }}</td>
          <td>{{ fila.gols_contra }}</td>
          <td>{{ fila.gols_favor - fila.gols_contra }}</td>
          <td>{{ fila.punts }}</td>
        </tr>
      </tbody>
    </table>

      <p v-if="classificacio.length === 0">No hi ha classificació per aquesta jornada.</p>
    </section>

    <section v-else-if="activeTab === 'Partits'">
      <div class="classificacio-controls">
        <button @click="anteriorJornada" :disabled="jornadaActual === 1">← Jornada anterior</button>
        <span class="jornada-title">Jornada {{ jornadaActual }}</span>
        <button @click="seguentJornada" :disabled="jornadaActual === jornadaMaxima">Jornada següent →</button>
        <button @click="editMode = !editMode">
          {{ editMode ? 'Finalitzar edició' : 'Editar resultats' }}
        </button>
      </div>

      <div v-if="partits.length" class="partits-container">
        <div v-for="partit in partits" :key="partit.id" class="partit-card">
          
          <div class="equip equip-local">
            <img :src="getEquipById(partit.equip_local_id).foto" class="logo-equip" />
            <span class="nom-equip">{{ getEquipById(partit.equip_local_id).nom }}</span>
          </div>

          <div class="marcador">
            <template v-if="editMode">
              <input
                type="number"
                class="input-gol"
                v-model.number="partit.gols_local"
                @input="onInputGols(partit)"
                min="0"
              />
              <span class="guio">-</span>
              <input
                type="number"
                class="input-gol"
                v-model.number="partit.gols_visitant"
                @input="onInputGols(partit)"
                min="0"
              />
            </template>
            <template v-else>
              <span class="marcador-text">
                {{ partit.gols_local }} - {{ partit.gols_visitant }}
              </span>
            </template>
          </div>

          <div class="equip equip-visitant">
            <span class="nom-equip">{{ getEquipById(partit.equip_visitant_id).nom }}</span>
            <img :src="getEquipById(partit.equip_visitant_id).foto" class="logo-equip" />
          </div>
        </div>
      </div>



      <p v-else>No hi ha partits per aquesta jornada.</p>
    </section>

    <section v-else-if="activeTab === 'Quadre'">
      <table class="quadre-taula" v-if="quadreEquips.length">
        <thead>
          <tr>
            <th></th>
            <th v-for="id in quadreEquips" :key="id">
              <img :src="getEquipById(id).foto" class="quadre-logo" />
            </th>
          </tr>
        </thead>

        <tbody>
           <tr v-for="(idRow, i) in quadreEquips" :key="idRow">
            <th>
              <img :src="getEquipById(idRow).foto" class="quadre-logo" />
            </th>

            <td v-for="(res, j) in quadreResultat[i]" :key="j"
                :class="{ diag:i===j }">
              <span v-if="i !== j">
                {{ res ?? '–' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-else>No hi ha resultats.</p>
    </section>

    <section v-else-if="activeTab === 'Històric'">
      <div class="historic-container">
        <canvas id="historicChart"></canvas>
      </div>
    </section>
  </div>

  <div v-if="showModal" class="modal-overlay" @click.self="tancarModal">
    <div class="modal">
      <h3>Vincula equips</h3>
      <form @submit.prevent="vincularEquipsATemporada">
        <label class="select-label">
          Equip:
          <select v-model="form.equip_id" required>
            <option disabled value="">Selecciona un equip</option>
            <option v-for="e in equips" :key="e.id" :value="e.id">{{ e.nom }}</option>
          </select>
        </label>
        <div v-if="form.equip_id">
          <img
            v-if="equips.find(x => x.id === form.equip_id)?.foto"
            :src="equips.find(x => x.id === form.equip_id).foto"
            style="max-width:100px;max-height:100px;margin:0.5rem 0"
          />
        </div>
        <div class="modal-actions">
          <button type="button" @click="tancarModal">Cancel·la</button>
          <button type="submit">Vincula</button>
        </div>
      </form>
    </div>
  </div>

  <div v-if="showModalPartits" class="modal-overlay" @click.self="tancarModalPartit">
    <div class="modal">
      <h3>Crea partit</h3>
      <form @submit.prevent="crearPartit">
        <label class="select-label">
          Local:
          <select v-model="formPartits.equipLocal" required>
            <option disabled value="">Selecciona un equip</option>
            <option v-for="e in equipsATemporada" :key="e.id" :value="e.id">{{ e.nom }}</option>
          </select>
        </label>
        <label class="select-label">
          Visitant:
          <select v-model="formPartits.equipVisitant" required> 
            <option disabled value ="">Selecciona un equip</option>
            <option v-for="e in equipsATemporada" :key="e.id" :value="e.id">{{ e.nom }}</option>
          </select>
        </label>
        <label class="select-label">
          Jornada:
          <select v-model="formPartits.jornada" required >
            <option disable value=""> Selecciona una jornada</option>
            <option v-for="j in jornadaMaxima" :key="j" :value="j">
              Jornada {{ j }}
            </option>
          </select>
        </label>
        <div class="modal-actions">
          <button type="button" @click="tancarModalPartit">Cancel·la</button>
          <button type="submit">Vincula</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  padding: 0 2rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.header-buttons {
  display: flex;
  gap: 0.5rem;
}
.logo {
  width: 50px;
  height: 50px;
  object-fit: contain;
  border-radius: 6px;
}
.crear-btn {
  background: #1976d2;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}
.crear-btn:hover { background:#1565c0; }

.tabs {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  border-bottom: 2px solid #ccc;
}
.tab-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 600;
  border-bottom: 3px solid transparent;
}
.tab-btn.active {
  border-color: #1976d2;
  color: #1976d2;
}

.equip-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}
.equip-logo {
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-right: 0.5rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 360px;
}
.select-label {
  display: block;
  margin-bottom: 1rem;
  font-weight: 600;
}
.modal select {
  width: 100%;
  padding: 0.4rem;
  border: 2px solid #000;
  border-radius: 4px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
.modal-actions button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  width: 48%;
  margin-right: 4%;
  transition: background-color 0.2s;
}

.modal-actions button:last-child {
  margin-right: 0;
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

.equips-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-top: 1rem;
}

.equip-card {
  border: 2px solid black;
  border-radius: 12px;
  background-color: #fdfdfd;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.menu-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.dropdown-menu {
  position: absolute;
  top: 1.8rem;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

.dropdown-menu button {
  display: block;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.dropdown-menu button:hover {
  background-color: #f5f5f5;
}

.equip-logo-top {
  width: 60px;
  height: 60px;
  object-fit: contain;
  margin-bottom: 0.75rem;
  margin-top: 0.75rem;
}

.equip-nom {
  font-weight: 600;
  font-size: 1.05rem;
  text-align: center;
}

.classificacio-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.jornada-title {
  font-weight: bold;
  font-size: 1.2rem;
}

.classificacio-taula {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  border: none;
}

.classificacio-taula th,
.classificacio-taula td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
}


.classificacio-taula th {
  background-color: #f0f0f0;
  padding: 0.5rem 1rem; 
  text-align: center;
}

.classificacio-taula td {
  padding: 0.5rem 0; 
  text-align: center;
  border: none;
}

.partits-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.partit-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 2px solid #ccc;
  border-radius: 12px;
  padding: 1rem;
  background: #fefefe;
  width: 100%;
  margin-bottom: 1rem;
}


.equip {
  display: flex;
  align-items: center;
  width: 45%;
  min-width: 0;
}

.equip-local {
  justify-content: flex-start;
}

.equip-visitant {
  justify-content: flex-end;
}

.equip-visitant > .nom-equip {
  order: 1;
  margin-left: 0.5rem;
}

.equip-visitant > .logo-equip {
  order: 2;
}


.marcador {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 10%;
  min-width: 80px;
  font-family: monospace;
  font-size: 1.2rem;
  font-weight: bold;
  gap: 0.25rem;
}

.input-gol {
  width: 2.5rem;
  height: 2rem;
  text-align: center;
  font-family: monospace;
  font-size: 1.2rem;
  border: 1px solid #aaa;
  border-radius: 4px;
  padding: 0.2rem;
  line-height: 1.2rem;
}

.guio {
  width: 1rem;
  text-align: center;
  font-family: monospace;
  line-height: 1.2rem;
  height: 2rem;
}

.logo-equip {
  width: 40px;
  height: 40px;
  object-fit: contain;
  flex-shrink: 0;
}

.nom-equip {
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.quadre-taula {
  border-collapse: collapse;
  margin-top: 1.5rem;
  width: 100%;
}

.quadre-taula th,
.quadre-taula td {
  border: 1px solid #ccc;
  width: 60px;
  height: 60px;
  text-align: center;
  vertical-align: middle;
  font-family: monospace;
}

.quadre-logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.diag {
  background: #000;
}

.historic-container {
  height: 600px;
  width: 100%;
  padding: 1rem;
}

</style>
