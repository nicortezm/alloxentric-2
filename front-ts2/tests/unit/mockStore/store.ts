import { createStore } from 'vuex'

export const storeRole1 = createStore({
    
    state() {
      return {
        user : {
            isAuthenticated: true,
            name: "jorge",
            idToken: "asdasdasdasdasd",
            accessToken: "adsasdasdasd",
            rol: "role1"
        }
      } 
    },
  })



export const storeRole2 = createStore({
    
    state() {
      return {
        user : {
            isAuthenticated: true,
            name: "jorge",
            idToken: "asdasdasdasdasd",
            accessToken: "adsasdasdasd",
            rol: "role2"
        }
      } 
    },
})
  