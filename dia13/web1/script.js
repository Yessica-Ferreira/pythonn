boton = document.getElementById("btn-iniciar")

boton.addEventListener("click",validar)

function validar(){
    usuario = document.getElementById("usuario")
    if(usuario.value != ""){
      alert("Enviando datos...")
}else{
    alert("El campo no puede estar vacio")
}
}