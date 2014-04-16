
	function Calendario()
	{		
		$(".keys").datepicker({                
			showOn: "both",
				dateFormat: "dd-mm-yy",
			buttonImage: "/media/imgs/calendar.gif", 
			buttonImageOnly: true 
		}).attr("readonly", "readonly");
	}
	function Dialogo()
	{				
		$("#dialog").dialog( {width:660, 
			height:650, modal:true,
			/*show: 'slide', */ hide: 'slide',
			resizable: false, autoOpen: false});
	}

	function MuestroDialogo()
	{
		GraboCookiesPaciente('');		
		fin.selectedIndex=inicio.selectedIndex+1;
		$("#dialog").dialog('open');
	}
  
	function buscoNombre()
	{
	      BuscoNombreAjax($("#nombre").attr("value").toUpperCase(),$("#paterno").attr("value").toUpperCase(),$("#materno").attr("value").toUpperCase());
	}
		
  function cambioFin()
  {	
	fin.selectedIndex=inicio.selectedIndex+1;
  }
  
  function Valido()
  {	
	return fin.selectedIndex>inicio.selectedIndex;/*$("#fin option").index($("#fin option:selected")) >
	   $("#inicio option").index($("#inicio option:selected"))*/
  }
  
  function ValidoFin()
  {
	var bRetorno=false;

	if(!Valido())
	{		
		cambioFin();		
	}
	else
	{
		bRetorno=true;
	}
	//alert(bRetorno);
	return bRetorno;
  }
  function ValidoInput()
  {
	var bRetorno=true;
	$(".validable").each(		
		function() {			
			if($(this).attr("value").length==0)	
			{	
				$(this).addClass("error");
			}
			else
			{
				$(this).removeClass("error");
			}
	});
	if($("input").hasClass("error"))
	{		
		$("#errorCaptura").text("Faltan capturar algunos campos obligatorios");
		$("#errorCaptura").fadeIn("slow");
		bRetorno=false;
	}
	else
	{
		LimpioMensaje();
	}
	return bRetorno;
  }
  function LimpioMensaje()
  {
	$("#errorCaptura").text("");
	$("#errorCaptura").fadeOut("slow");
  }
  var pacientenuevo;
  function GrabarCita(PacienteNuevo)
  {
	pacientenuevo=PacienteNuevo;
	if(Valido())
	{
		if(ValidoInput())
		{
			
			if(GetCookie("pacn")==null && !PacienteNuevo) //si es paciente nuevo no puedo buscar porque no existe en la bd
			{
				buscoNombre();
			}
			else
			{
				ExisteCita();//Compruebo si existe un cita en ese horar, en caso contrario la registro					
			}
		}
	}
	else
	{
		cambioFin();
		alert("La hora final de la cita debe ser mayor que la hora inicial");
	}
  }
  function ExisteCita()
  {
	var fecha=$("#fechacita").attr("value");
	var inicio=$("#inicio").attr("value");
	var fin =$("#fin").attr("value");
	var doctor=$("#dr").attr("value");
	ajax={
		type: "POST",
		async:true,
		dataType:"json",
		url:"/buscocita",
		data:"fecha="+fecha+"&inicio="+inicio+"&fin="+fin+"&dr="+doctor,			
		error: function ()
				{
					alert("Ocurrio un error con la busqueda de la Cita");
					$("#buscando").html("");
				},            
		success:DatosCitaValidad
	};	
	$.ajax(ajax);//llamo la funcion con JQUERY  
  }

 
  function DatosCitaValidad(datos)
  {
	for (obj in datos)
	{
		if(datos[obj].citas==0)
		{
			GraboDatos();
		}
		else
		{
			alert("Ya existe una cita previa en dicho horario");
		}
	}	
  }
  function GraboDatos()
  {
	/*OJO ver como se va a grabar cuando se es secre*/
	var duracion=document.getElementById("fin").selectedIndex-document.getElementById("inicio").selectedIndex;
	var nombre=$("#nombre").attr("value");
	var paterno=$("#paterno").attr("value");
	var materno=$("#materno").attr("value");
	var fecha=$("#fechacita").attr("value");
	var inicio=$("#inicio").attr("value");
	var fin =$("#fin").attr("value");
	var doctor=$("#dr").attr("value");
	var paciente=GetCookie("pacn");
	var str=""
	if (paciente!=null){
	    str=paciente.split("=");
	}
	
	paciente=str[1];	
	var pacienteNuevo=pacientenuevo
	ajax={
		type: "POST",
		async:true,
		//dataType:"json",
		url:"/grabocita",
		data:   "nombre="+nombre+" "+paterno+" "+materno+
			"&fecha="+fecha+"&inicio="+inicio+"&fin="+fin+
			"&duracion="+duracion+"&pacientenuevo="+pacientenuevo+
			"&doctor="+doctor+"&paciente="+paciente,			
		error: function ()
				{
					alert("Ocurrio un error con el registro de los datos de la Cita");
					$("#buscando").html("");
				},            
		success:ReciboDatosCita
	};       		
	$.ajax(ajax);//llamo la funcion con JQUERY  
  }
function ReciboDatosCita(datos)
{
	$("#errorCaptura").text("Datos grabados con exito");
	$("#errorCaptura").fadeIn("slow");
	Limpio();
}

function Limpio()
{
	$(".limpiar").attr("value","");
	GraboCookiesPaciente("");
	inicio.selectedIndex=0;
	fin.selectedIndex=0;
	var Hoy = new Date();
	var fecha=Hoy.getDay().toString()+"-"+Hoy.getMonth().toString()+"-"+Hoy.getFullYear().toString();
	$("#fecha").attr("value",fecha)
}