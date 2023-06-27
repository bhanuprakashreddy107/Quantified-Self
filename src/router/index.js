import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import signup from '../components/signup.vue'
import Login from '../components/Login.vue'
import AddTracker from '../components/AddTracker.vue'
import SeeTrackers from '../components/SeeTrackers.vue'
import AddLog from '../components/AddLog.vue'
import ViewData from '../components/ViewData.vue'
import Logout from '../components/Logout.vue'
import Forgot from '../components/Forgot.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/signup',
      name: 'signup',
      component: signup
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/addTracker',
      name: 'AddTracker',
      component: AddTracker
    },
    {
      path: '/seeTrackers',
      name: 'SeeTrackers',
      component: SeeTrackers
    },
    {
      path: '/addLog/:id',
      name: 'AddLog',
      component: AddLog
    },
    {
      path: '/viewData/:id',
      name: 'ViewData',
      component: ViewData
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout
    },
    {
      path: '/forgot',
      name: 'Forgot',
      component: Forgot
    },
    
  ]
})

export default router
