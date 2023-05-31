<!DOCTYPE html>
<html>
<head>
	<title>Dashboard</title>
    <link rel="stylesheet" href="../static/style.css">
    <link rel="stylesheet" href="{{ url_for('static',filename='style.css') }}">

</head>
<body>
	<div id="wrapper">
<div>
        <a class="logout" href="{{url_for('logout')}}">Sign out</a>
		<div class="header">
        <h1>Dashboard</h1>
    </div>

    
<ul>
    <li><a href="/">Show All</a></li>
    <br>
    {% set seen_mac_addresses = [] %}

    {% for item in Protocoldata %}
        {% if item.MacAdress not in seen_mac_addresses %}
            <li><a href="?show={{item.MacAdress}}">{{ item.MacAdress }}</a></li>
            {% set _ = seen_mac_addresses.append(item.MacAdress) %}
        {% endif %}
    {% endfor %}

   {% for pitem in Portdata %}
        {% if pitem.MacAdress not in seen_mac_addresses %}
            <li><a href="?show={{pitem.MacAdress}}">{{ pitem.MacAdress }}</a></li>
            {% set _ = seen_mac_addresses.append(pitem.MacAdress) %}
        {% endif %}
    {% endfor %}
</ul>
    


    <div class="plot1">
        <img class="charts" src='data:image/png;base64,{{plot1}}' />
    </div>
{% set portdis = true %}
<!-- Find id fra urlen -->
{% set get_id = request.args.get('show') %}

<!-- Hvis der findes et id i urlen -->
{% if get_id is not none: %}

<!-- Vis specifik underside  -->

{% for item in Protocoldata %}


{% if item.MacAdress == get_id  %}
<hr>
<div class="block">


        <h2> IP Address: {{ item.IpAdress }} </h2>
        <h2> MAC Address: {{ item.MacAdress }} </h2>
        <h2> ID: {{ item.id }} </h2>
        <h2> Registered: {{ item.Datetime }} </h2>


<div class="table_div">
<h3> SSL TSL </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>

{% autoescape false %}
  {{ item.SSLTSL | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>


<div class="table_div">
<h3> HeartBleed </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>

{% autoescape false %}
  {{ item.HeartBleedVulnability | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}

</table>
</div>
<div class="table_div">
<h3> Protocol </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>

{% autoescape false %}
  {{ item.Protocols | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>


<!----------------------------------------------------------------------------------------------------------------------------------------------------------->
{% for pitem in Portdata %}
{% if pitem['MacAdress'].strip() == get_id %}
{% set portdis = true %}

<div class="table_div">
<h3> Ports </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>

{% autoescape false %}
{{ pitem.Ports | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>
<div class="invisible">


{% endif %}
{% endfor %}


{% endif %}
{% endfor %}

<!------------ Specifik underside, der kun har Portscan ------------->

{% if portdis %}
{% for port_item in Portdata %}
{% if port_item.MacAdress == get_id %}


<hr>
<div class="block">


        <h2> IP Address: {{ port_item.IpAdress }} </h2>
        <h2> MAC Address: {{ port_item.MacAdress }} </h2>
        <h2> ID: {{ port_item.id }} </h2>
        <h2> Registered: {{ port_item.Datetime }} </h2>




{% autoescape false %}
<div class="table_div">
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>
{{ port_item.Ports | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
</table>
</div>
{% endautoescape %}


{% endif %}



{% endfor %}
{% endif %}




{% else %} 

<!-------------  Vis alt data  --------------->
      {% set seen_mac_addresses = [] %}
    {% for item in Protocoldata %}
        {% if item.MacAdress not in seen_mac_addresses %}
<hr>
<div class="block">

        <h2> IP Address: {{ item.IpAdress }} </h2>
        <h2> MAC Address: {{ item.MacAdress }} </h2>
        <h2> ID: {{ item.id }} </h2>
        <h2> Registered: {{ item.Datetime }} </h2>

<div class="table_div">
<h3> SSL TSL </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>
{% autoescape false %}
  {{ item.SSLTSL | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>


<div class="table_div">
<h3> HeartBleed </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>
{% autoescape false %}
  {{ item.HeartBleedVulnability | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>


<div class="table_div">
<h3> Protocol </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>
{% autoescape false %}
  {{ item.Protocols | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table>
</div>


{% for port_item in Portdata %}

{% if port_item.MacAdress == item.MacAdress %}

<div class="table_div">
<h3> Ports </h3>
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>

{% autoescape false %}
{{ port_item.Ports | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
{% endautoescape %}
</table> 
</div>
        {% else %}
 
</div>
        {% endif %}
    {% endfor %}

{% set _ = seen_mac_addresses.append(item.MacAdress) %}
        {% endif %}
    {% endfor %}

<!--------------- Slut og gaa over i ports only ---------------->

{% for port_item in Portdata %}
{% if port_item.MacAdress not in seen_mac_addresses %}
<hr>
<div class="block">


        <h2> IP Address: {{ port_item.IpAdress }} </h2>
        <h2> MAC Address: {{ port_item.MacAdress }} </h2>
        <h2> ID: {{ port_item.id }} </h2>
        <h2> Registered: {{ port_item.Datetime }} </h2>




{% autoescape false %}
<div class="table_div">
<table>
<tr>
<th>Port</th>
<th>Status</th>
</tr>
{{ port_item.Ports | replace(":", "</td><td>") | replace(",", "</tr><tr><td>") | replace('"', '') | replace('{', '<td>') | replace("}", "") }}
</table>
</div>

{% set _ = seen_mac_addresses.append(port_item.MacAdress) %}
{% endautoescape %}


{% endif %}

{% endfor %}

{% endif %}



      </div>
<hr>



    


   	 </ul>

	</div>
</body>
</html>
