<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import EquipService from '../services/EquipsServices'
import TemporadaService from '../services/TemporadesServices'
import CompetitionService from '../services/CompetitionServices'
import JugadorService from '../services/JugadorsServices.js'
import CountryService from '../services/CountryServices.js'
import PlantillaService from '../services/PlantillaServices.js'

const route = useRoute()
const equip = ref(null)
const activeTab = ref('Plantilla')
const temporades = ref([])
const temporadaSeleccionada = ref(null)
const competicio = ref(null)
const competicioId = route.query.competicio_id
const showModalPlantilla = ref(false)
const jugadors = ref([])
const paisos = ref([])
const seleccionats = ref([])
const filtreModal = ref('')
const plantilla = ref([])
const ordrePosicions = ['POR', 'DEF', 'MIG', 'DAV']
const posicioLabels = {
  POR: 'Porters',
  DEF: 'Defenses',
  MIG: 'Migcampistes',
  DAV: 'Davanters'
}
const showModalDorsals = ref(false)
const jugadorEditant = ref(null)
const dorsalEdit = ref(null)
const dorsalStartEdit = ref(null)
const dorsalEndEdit = ref(null)
const dorsalIdEdit = ref(null)

onMounted(async () => {
  const id = route.params.id
  paisos.value = await CountryService.getAll()
  equip.value = await EquipService.getById(id)
  console.log(competicioId)
  if (competicioId) {
    competicio.value = await CompetitionService.getById(competicioId)
    temporades.value = await TemporadaService.getByCompeticio(competicioId)
  }
    
  if (temporades.value.length) {
    temporadaSeleccionada.value = temporades.value[0].id
  }
  console.log(temporades.value)
  }
)

const temporadesOrdenades = computed(() =>
  [...temporades.value].sort((a, b) => b.any_inici - a.any_inici)
)

async function obrirModalPlantilla() {
  jugadors.value = await JugadorService.getAll()
  seleccionats.value = plantilla.value.map(j => j.id)
  showModalPlantilla.value = true
}
function tancarModalPlantilla() {
  showModalPlantilla.value = false
}

const jugadorsFiltratsModal = computed(() =>
  jugadors.value.filter(j =>
    (j.sobrenom || `${j.nom} ${j.cognom_1}` || '')
      .toLowerCase()
      .includes(filtreModal.value.toLowerCase())
  )
)

const jugadorsPerPosicio = computed(() => {
  const grups = {}
  for (const jugador of plantilla.value) {
    const pos = jugador.posicio || 'Altres'
    if (!grups[pos]) grups[pos] = []
    grups[pos].push(jugador)
  }
  return grups
})

async function carregarPlantilla() {
  if (equip.value && temporadaSeleccionada.value) {
    try {
      plantilla.value = await PlantillaService.getByEquipITemporada(
        equip.value.id,
        temporadaSeleccionada.value
      )
    } catch (e) {
      plantilla.value = []
    }
  }
}

watch([temporadaSeleccionada, equip], carregarPlantilla, { immediate: true })

async function guardarPlantilla() {
  if (!equip.value || !temporadaSeleccionada.value) return
  try {
    await PlantillaService.crearPlantilla(
      equip.value.id,
      temporadaSeleccionada.value,
      seleccionats.value
    )
    await carregarPlantilla()
    showModalPlantilla.value = false
    alert('Plantilla desada correctament!')
  } catch (e) {
    alert('Error en desar la plantilla')
  }
}

function obrirModalDorsals(jugador) {
  console.log(jugador.id_plantilla)
  jugadorEditant.value = jugador
  if (jugador.dorsals.length > 0) {
    const d = jugador.dorsals[0]
    dorsalEdit.value = d.dorsal
    dorsalStartEdit.value = d.dorsal_start_jornada
    dorsalEndEdit.value = d.dorsal_end_jornada
    dorsalIdEdit.value = jugador.id_plantilla
  } else {
    dorsalEdit.value = null
    dorsalStartEdit.value = null
    dorsalEndEdit.value = null
    dorsalIdEdit.value = jugador.id_plantilla
  }
  showModalDorsals.value = true
}

function tancarModalDorsals() {
  showModalDorsals.value = false
}

async function guardarDorsals() {
  try {
    if (dorsalIdEdit.value) {
      console.log(dorsalIdEdit.value, dorsalEdit.value, dorsalStartEdit.value, dorsalEndEdit.value)
      await PlantillaService.assignarDorsal(dorsalIdEdit.value, dorsalEdit.value, dorsalStartEdit.value, dorsalEndEdit.value)
    } else {
      alert('No es pot guardar un dorsal nou des d\'aquí. Utilitza la modificació de plantilla.')
    }
    await carregarPlantilla()
    showModalDorsals.value = false
  } catch (e) {
    alert('Error actualitzant dorsals')
  }
}
</script>

<template>
  <div class="main-container" v-if="equip">
    <header class="header">
      <div class="header-left">
        <img v-if="equip.foto" :src="equip.foto" alt="Foto equip" class="logo" />
        <h2>{{ equip.nom }}</h2>
      </div>
    </header>

    <nav class="tabs">
      <button
        v-for="tab in ['Plantilla', 'Partits', 'H2H']"
        :key="tab"
        :class="['tab-btn', { active: activeTab === tab }]"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </nav>

    <section v-if="activeTab === 'Plantilla'">
      <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 1rem; gap: 1rem;">
        <select v-model="temporadaSeleccionada" class="temporada-select">
          <option v-for="t in temporadesOrdenades" :key="t.id" :value="t.id">
            {{ t.any_inici }}-{{ t.any_fi }}
          </option>
        </select>
        <button class="modificar-btn" @click="obrirModalPlantilla">Modificar plantilla</button>
      </div>
      <table class="plantilla-taula">
        <thead>
          <tr>
            <th style="text-align: center;">Dorsal</th>
            <th style="text-align: center;">Foto</th>
            <th style="text-align: center;">Nom</th>
            <th style="text-align: center;">Posició</th>
            <th style="text-align: center;">País</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="posicio in ordrePosicions" :key="posicio">
            <tr>
              <td :colspan="5" class="posicio-separador">{{ posicioLabels[posicio] || posicio }}</td>
            </tr>
            <tr v-for="jugador in jugadorsPerPosicio[posicio] || []" :key="jugador.id">
              <td @click="obrirModalDorsals(jugador)" style="text-align: center; cursor: pointer;">
                <div class="dorsal-box">
                  <span v-for="(d, index) in jugador.dorsals" :key="d.id">
          
                    {{ d || 'N/A' }}
                    <span v-if="index < jugador.dorsals.length - 1">, </span>
                  </span>
                </div>
              </td>
              <td style="text-align: center;">
                <img v-if="jugador.url_imatge" :src="jugador.url_imatge" alt="Foto jugador" style="max-width:80px; max-height:80px; border-radius:12px;">
              </td>
              <td style="text-align: center;">
                <div class="field-box">
                  {{ jugador.sobrenom || `${jugador.nom} ${jugador.cognom_1}` }}
                </div>
              </td>
              <td style="text-align: center;">
                <div class="field-box">
                  {{ jugador.posicio }}
                </div>
              </td>
              <td style="text-align: center;">
                <img
                  v-if="paisos.find(p => String(p.id) === String(jugador.nacionalitat))?.url_imatge"
                  :src="paisos.find(p => String(p.id) === String(jugador.nacionalitat)).url_imatge"
                  style="max-width:32px; max-height:32px; border-radius:8px; background:#fff;"
                />
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </section>
    <section v-else-if="activeTab === 'Partits'">
      <!-- Contingut dels partits -->
    </section>
    <section v-else-if="activeTab === 'H2H'">
      <!-- Contingut H2H -->
    </section>

    <!-- Modal per modificar plantilla -->
    <div v-if="showModalPlantilla" class="modal-overlay" @click.self="tancarModalPlantilla">
      <div class="modal-gran-centrat">
        <h3>Selecciona jugadors per la plantilla</h3>
        <input
          v-model="filtreModal"
          type="text"
          placeholder="Cerca jugador..."
          style="margin-bottom: 1rem; padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #ccc; width: 100%;"
        />
        <table class="plantilla-taula">
          <thead>
            <tr>
              <th>Foto</th>
              <th>Nom</th>
              <th>Posició</th>
              <th>País</th>
              <th>Incloure</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="jugador in jugadorsFiltratsModal" :key="jugador.id">
              <td>
                <img :src="jugador.url_imatge" alt="foto" style="width:50px;height:50px;border-radius:8px;" />
              </td>
              <td>{{ jugador.sobrenom || `${jugador.nom} ${jugador.cognom_1}` }}</td>
              <td>{{ jugador.posicio }}</td>
              <td>
                <img
                  v-if="paisos.find(p => p.id === jugador.nacionalitat)?.url_imatge"
                  :src="paisos.find(p => p.id === jugador.nacionalitat).url_imatge"
                  :alt="paisos.find(p => p.id === jugador.nacionalitat)?.nom"
                  style="max-width:32px; max-height:32px; border-radius:8px; background:#fff;"
                />
              </td>
              <td>
                <input type="checkbox" v-model="seleccionats" :value="jugador.id" />
              </td>
            </tr>
          </tbody>
        </table>
        <div class="modal-actions">
          <button @click="tancarModalPlantilla" type="button" class="btn-cancelar">Cancel·la</button>
          <button type="button" class="btn-desar" @click="guardarPlantilla">Desa plantilla</button>
        </div>
      </div>
    </div>

    <!-- Modal per editar dorsals -->
    <div v-if="showModalDorsals" class="modal-overlay" @click.self="tancarModalDorsals">
      <div class="modal-gran-centrat">
        <h3>Editar dorsals per {{ jugadorEditant?.sobrenom || `${jugadorEditant?.nom} ${jugadorEditant?.cognom_1}` }}</h3>
        <div style="margin-bottom: 1rem; display: flex; gap: 1rem; align-items: center;">
          <label>Dorsal: <input v-model.number="dorsalEdit" type="number" style="width: 60px;" /></label>
          <label>Jornada Inicial: <input v-model.number="dorsalStartEdit" type="number" style="width: 100px;" /></label>
          <label>Jornada Final: <input v-model.number="dorsalEndEdit" type="number" style="width: 100px;" /></label>
        </div>
        <div class="modal-actions">
          <button @click="tancarModalDorsals" class="btn-cancelar">Cancel·la</button>
          <button @click="guardarDorsals" class="btn-desar">Desa</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  padding: 0 2rem;
}
.header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.logo {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 12px;
  background: #fff;
  border: 2px solid #eee;
}
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
.tab-content,
section {
  background: #fff;
  border-radius: 0 6px 6px 6px;
  padding: 2rem;
  min-height: 200px;
}
.plantilla-taula {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.plantilla-taula th,
.plantilla-taula td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}
.plantilla-taula th {
  background-color: #f4f4f4;
  font-weight: 600;
}
.modificar-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.modificar-btn:hover {
  background-color: #155a8a;
}
.temporada-select {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
}
.modal-overlay {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-gran {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  width: 900px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 32px rgba(0,0,0,0.2);
}
.modal-gran-centrat {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  width: 900px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 32px rgba(0,0,0,0.2);
  margin: auto;
  display: flex;
  flex-direction: column;
}
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.jugadors-select,
.paisos-select {
  margin-bottom: 1rem;
}
.guardar-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.guardar-btn:hover {
  background-color: #45a049;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
.btn-cancelar {
  background-color: #e53935;
  color: white;
  border: none;
  padding: 0.7rem 2rem;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-cancelar:hover {
  background-color: #b71c1c;
}
.btn-desar {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 0.7rem 2rem;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-desar:hover {
  background-color: #1565c0;
}
.posicio-separador {
  background: #222;
  color: #fff;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.3rem 0.5rem;
  border: none;
  height: 28px;
  letter-spacing: 1px;
}
.dorsal-box {
  background: #ccc;
  padding: 4px 8px;
  display: inline-block;
  border-radius: 4px;
  font-weight: bold;
}
.field-box {
  background: #ccc;
  padding: 4px 8px;
  display: inline-block;
  border-radius: 4px;
  font-weight: bold;
}
</style>