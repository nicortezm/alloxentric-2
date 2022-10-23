import { createStore } from 'vuex'


export default createStore({
  state: {
    user: {
      isAuthenticated: false,
      name: "",
      idToken: "",
      accessToken: "",
      rol: ""
    }
  },
  getters: {
  },


  mutations: {
    
    logout(state) {
      state.user.isAuthenticated = false;
      state.user.name = "";
      state.user.idToken = "";
      state.user.accessToken = "";
      state.user.rol = ""
    },

    login(state, payload) {
      state.user.isAuthenticated = true;
      state.user.idToken = payload.idToken;
      state.user.accessToken = payload.accessToken;
    },

    setName(state, payload) {
      state.user.name = payload.name;
    }
  },



  actions: {
  },



  modules: {
  }
})
