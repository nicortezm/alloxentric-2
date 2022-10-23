import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { Role1Guard, Role2Guard } from './guardRol';
import Keycloak from 'keycloak-js';




export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    props: Keycloak
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/filter',
    name: 'filter',
    beforeEnter: [ Role1Guard ], 
    component: () => import(/* webpackChunkName: "Filters" */ '../views/FilterView.vue'),
  },
  {
    path: '/tags',
    name: 'tags',
    beforeEnter: [ Role2Guard ], 
    component: () => import(/* webpackChunkName: "Tags" */ '../views/TagsView.vue')
  },
  {
    path: '/details/:endpoint',
    name: 'details',
    component: () => import(/* webpackChunkName: "Tags" */ '../views/DetailsView.vue'),
    props: ( route ) => {
      console.log( route )
      return {
          endpoint: route.params.endpoint
      }
    } 
  },

  { 
    path: '/:pathMatch(.*)*', 
    component: HomeView
  }    
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})










export default router
