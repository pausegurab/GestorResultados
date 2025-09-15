// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Welcome from '../components/Welcome.vue'
import Temporades from '../components/Temporades.vue'
import Equips from '../components/Equips.vue'
import Competicio from '../components/VistaCompeticio.vue'
import Jugadors from '../components/Jugadors.vue'
import EquipDetall from '../components/EquipDetall.vue'

const routes = [
  { path: '/', component: Welcome },
  { path: '/temporades', component: Temporades },
  { path: '/equips', component: Equips},
  { path: '/equips/:id', name: 'equip-detall', component: EquipDetall},
  { path : '/vistaCompeticio', component: Competicio},
  { path: '/jugadors', component: Jugadors}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router