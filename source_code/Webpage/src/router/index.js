import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Register from '@/views/Register'
import Booking from '@/views/Booking'
import Profile from '@/views/Profile'
import Order from '@/views/Order'
import FilmDetail from '@/views/Film/film-detail'
import FilmFilter from '@/views/Film/film-filter'
import FilmSearch from '@/views/Film/film-search'

Vue.use(Router)

let routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    active: 0
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    active: -1
  },
  {
    path: '/booking/:id',
    name: 'Booking',
    component: Booking,
    active: -1
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    active: -1
  },
  {
    path: '/orders',
    name: 'Order',
    component: Order,
    active: -1
  },
  {
    path: '/films',
    name: 'FilmFilter',
    component: FilmFilter,
    active: 1
  },
  {
    path: '/film/:id',
    name: 'FilmDetail',
    component: FilmDetail,
    active: -1
  },
  {
    path: '/search',
    name: 'FilmSearch',
    component: FilmSearch,
    active: -1
  }
]

const router = new Router({
  mode: 'history',
  routes: routes
})

router.afterEach((to, from, next) => {
  window.scroll(0, 0)
})

export default router
