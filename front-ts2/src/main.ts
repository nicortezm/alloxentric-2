import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Keycloak, { KeycloakOnLoad } from 'keycloak-js';

//createApp( App ).use( store ).use( router ).mount( '#app' )

const initOptions = {
  url: process.env.VUE_APP_KEYCLOAK_URL, 
  realm: process.env.VUE_APP_KEYCLOAK_REALM, 
  clientId: process.env.VUE_APP_KEYCLOAK_CLIENT, 
  onLoad: "login-required" as KeycloakOnLoad
}


const keycloak: any = new Keycloak(initOptions);

keycloak.init({ onLoad: initOptions.onLoad }).then(( auth : any ) => {
  
  if (!auth) {
    window.location.reload();
  } 
  console.log("Authenticated");

  createApp( App, { keycloak: keycloak } ).use(store).use(router).mount('#app')

  localStorage.setItem('rol',keycloak.resourceAccess.xentric_base.roles )
  localStorage.setItem('token', keycloak.token );

  // console.log( keycloak.token );
  

  let payload: any = {
    idToken: keycloak.idToken,
    accessToken: keycloak.token
  }

  if(( keycloak.token && keycloak.idToken != '' ) && (keycloak.idToken != '')){

    store.commit("login", payload)
    
    payload = { name: keycloak.tokenParsed.preferred_username }
    store.commit("setName", payload)
    
  }else{

    const payloadRefreshedTokens = {
      idToken: "",
      accessToken: ""
    }
    store.commit("login", payloadRefreshedTokens);
    store.commit("logout");
  }
  



  //Token Refresh
  setInterval(() => {
    keycloak.updateToken().then((refreshed) => {
      
      if (store.state.user.isAuthenticated != false ) {
        if (refreshed) {        
          let payloadRefreshedTokens = {
            idToken: keycloak.idToken,
            accessToken: keycloak.token
          }

          if ((keycloak.token && keycloak.idToken != '') && (keycloak.idToken != '')) {
            store.commit("login", payloadRefreshedTokens);
          }
          else {
            console.log("--> log: token refresh problems");  
            payloadRefreshedTokens = {
              idToken: "",
              accessToken: ""
            }
            store.commit("login", payloadRefreshedTokens);
            store.commit("logout");
          }
        }
      } else {
        console.log("--> log: logout isAuthenticated  =", store.state.user.isAuthenticated);
        
        const logoutOptions = { redirectUri : 'http://localhost:9000/' };

        keycloak.logout(logoutOptions).then((success) => {

              localStorage.removeItem('rol')
              console.log("--> log: logout success ", success );

        }).catch((error) => {
          
              console.log("--> log: logout error ", error );
        });
        store.commit("logout");
      }
      
    }).catch(() => {
      console.log("--> log: catch interval");
    });
  }, 1000)

}).catch(() => {
  //Vue.$log.error("Authenticated Failed");
  console.log("Authenticated Failed");
});
