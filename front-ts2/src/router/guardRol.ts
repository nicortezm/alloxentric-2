import Swal from "sweetalert2"




export const Role1Guard = ( to , from , next ) => {
    
    return new Promise ( () => {
     
        const rol = localStorage.getItem('rol')
  
        if( rol === 'role1' ) {

            console.log( 'Esta autorizado a filtrar')
            next()

        } else  {

            console.log( 'Bloqueado por el GuardRol' )

            next({ name: 'home'})

            Swal.fire({
                icon: 'warning',
                title: 'Rol invalido',
                text: `${rol} no tiene acceso a esa vista`,
              })
        }
    })
}



export const Role2Guard = ( to , from , next ) => {
    
    return new Promise ( () => {
     
        const rol = localStorage.getItem('rol')
  
        if( rol === 'role2' ) {

            console.log( 'Esta autorizado a etiquetar')
            next()

        } else  {

            console.log( 'Bloqueado por el GuardRol' )
            
            Swal.fire({
                icon: 'warning',
                title: 'Rol invalido',
                text: `${rol} no tiene acceso a esa vista`,
              })

            next({ name: 'home'})

        }
    })
}


