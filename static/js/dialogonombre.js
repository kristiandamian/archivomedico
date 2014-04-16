  function buscoNombre()
	{
	  GraboCookiesPaciente("");
	  BuscoNombreAjax($("#nombre").attr("value"),$("#paterno").attr("value"),$("#materno").attr("value"));
	}

    function DialogoNombre()
    {
	$("#dialogoNombre").dialog( {width: 660, 
	    height: 650 , modal:true,
	    /*show: 'slide', */ hide: 'slide',
	    resizable: false, autoOpen: false});	
    }
	
    function BuscoNombreAjax(Nombre,Paterno,Materno)
    {
	var nombre=Nombre.toUpperCase();
	var paterno=Paterno.toUpperCase();
	var materno=Materno.toUpperCase();
	
	ajax={
	    type: "POST",
	    async:true,
	    dataType:"json",
	    url:"/buscopaciente",
	    data:"nombre="+nombre+"&paterno="+paterno+"&materno="+materno,		
	    error: function ()
		    {
			    alert("Ocurrio un error con la busqueda del paciente");
			    $("#buscando").html("");
		    },            
	    success:ReciboDatosPaciente
	};
	$.ajax(ajax);//llamo la funcion con JQUERY  	
    }
    
    function ReciboDatosPaciente(datos)
    {
	$("#Nombres").empty();
	GraboCookiesPaciente('');
	for (obj in datos)
	{	    
	    //if(datos[obj].cantidad>1)	
	    {   
		for(var x=0; x<datos[obj].cantidad;x++)
		{		    
		    var cadena=datos[obj].nombres[x];
		    $("#Nombres").append("<option value='"+cadena+"'>"+cadena+"</option>");
		}		
		$("#dialogoNombre").dialog('open');
		$("#Nombres").attr('selectedIndex','0');//selecciono el primero por default
	    }
	}	
    }
	
    function Seleccionar(nombre,paterno,materno)
    {
	var nombreCompleto=$("#Nombres :selected").attr("value");
	var arraynombre=nombreCompleto.split("|");		
	$("#"+nombre).attr("value",arraynombre[0]);
	$("#"+paterno).attr("value",arraynombre[1]);
	$("#"+materno).attr("value",arraynombre[2]);
	usuario=arraynombre[4];
	GraboCookiesPaciente(usuario);
	$("#dialogoNombre").dialog('close');
	
	
    }
    
    function GraboCookiesPaciente(usuario)
    {
	if(usuario=="")
	{
	    Delete_Cookie("pacn","/","");
	}
	else
	{
	    document.cookie="pacn="+usuario;
	}	
	/*ajax={
	    type: "POST",
	    async:true,
	    //dataType:"json",
	    url:"/graboCPaciente",
	    data:"usuario="+usuario,		
	    error: function ()
		    {
			    alert("Ocurrio un error con la busqueda del paciente");
			    $("#buscando").html("");
		    }//,            
	    //success:ReciboDatosPaciente
	};
	$.ajax(ajax);//llamo la funcion con JQUERY  	*/
    }
    
    function Delete_Cookie( name, path, domain )
    {
	document.cookie = name + "=" +( ( path ) ? ";path=" + path : "") +
		(( domain ) ? ";domain=" + domain : "" ) +";expires=Thu, 01-Jan-1970 00:00:01 GMT";
    }
    
    function GetCookie(nombre)
   {
	var arg = name + "=";
	var alen = arg.length;
	var clen = document.cookie.length;
	var i = 0;
	
	if (i < clen) 
	{
		
		return document.cookie.substring(arg+1, clen);
	}
	return null;
    }
