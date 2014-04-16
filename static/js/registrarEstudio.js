function BorroUno(select)
{
    $(select+' :selected').remove();
}
function BorroTodos(select)
{
    $(select).empty();
}

function AgregoEstudio()
{
    cadena=$("#parametro").attr("value")+" | "+$("#resultado").attr("value")+" | "+$("#referencia").attr("value");
    if(trim(cadena).length>3)
    {
    	$("#datosEstudios").append("<option value='"+cadena+"'>"+cadena+"</option>");
	$("#parametro").attr("value","");
	$("#resultado").attr("value","");
	$("#referencia").attr("value","");
    }
}

function trim(cadena)
{
    for(i=0; i<cadena.length; )
    {
        if(cadena.charAt(i)==" ")
            cadena=cadena.substring(i+1, cadena.length);
	else
            break;
    }

    for(i=cadena.length-1; i>=0; i=cadena.length-1)
    {
	if(cadena.charAt(i)==" ")
            cadena=cadena.substring(0,i);
	else
            break;
    }
    return cadena;
}