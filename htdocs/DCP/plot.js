Ext.BLANK_IMAGE_URL = '../ext/resources/images/default/s.gif';

Ext.onReady(function(){
	var varStore = new Ext.data.Store({
		autoLoad	: false,
        proxy	: new Ext.data.HttpProxy({
            url     : '../json/dcp_vars.php'
        }),
        baseParams  : {'network': 'DCP'},
        reader: new Ext.data.JsonReader({
            root: 'vars',
            id: 'id'
        }, [
            {name: 'id', mapping: 'id'}
        ])
    });
	
	var varCB = new Ext.form.ComboBox({
		store			: varStore,
		displayField	: 'id',
		valueField		: 'id',
		width			: 100,
		mode			: 'local',
		fieldLabel		: 'Variable',
		emptyText		: 'Select Variable...',
		tpl				: new Ext.XTemplate(
		        '<tpl for="."><div class="search-item">',
	            '<span>[{id}]</span>',
	        '</div></tpl>'
	    ),
	    typeAhead		: false,
	    itemSelector	: 'div.search-item',
		hideTrigger		: false
	});
	var stationStore = new Ext.data.Store({
		autoLoad	: true,
        proxy	: new Ext.data.HttpProxy({
            url     : '../json/network.php'
        }),
        baseParams  : {'network': 'DCP'},
        reader: new Ext.data.JsonReader({
            root: 'stations',
            id: 'id'
        }, [
            {name: 'id', mapping: 'id'},
            {name: 'name', mapping: 'name'}
        ])
    });
	
	var stationCB = new Ext.form.ComboBox({
		store			: stationStore,
		displayField	: 'name',
		valueField		: 'id',
		width			: 300,
		mode			: 'local',
		triggerAction	: 'all',
		fieldLabel		: 'Station',
		emptyText		: 'Select Station...',
		tpl				: new Ext.XTemplate(
		        '<tpl for="."><div class="search-item">',
	            '<span>[{id}] {name}</span>',
	        '</div></tpl>'
	    ),
	    typeAhead		: false,
	    itemSelector	: 'div.search-item',
		hideTrigger		: false,
	    listeners		: {
			select: function(cb, record, idx){
				varStore.load({add: false, params: {station: record.id}});
				return false;
      		}
		}
	});
	var datepicker = new Ext.form.DateField({
		minValue	: new Date('1/1/2002'),
		maxValue	: new Date(),
		fieldLabel	: 'Start Date',
		emptyText	: "Select Date",
		allowBlank	: false
	});
	var dayInterval = new Ext.form.NumberField({
		minValue	: 1,
		maxValue	: 31,
		value		: 5,
		width		: 30,
		fieldLabel	: 'Number of Days'
	});
	
	function updateImage(){
		ds = datepicker.getValue();
		ds2 = ds.add(Date.DAY, dayInterval.getValue());
		url = String.format('plot.php?station={0}&sday={1}&eday={2}&var={3}',
				stationCB.getValue(), ds.format('Y-m-d'), 
				ds2.format('Y-m-d'), varCB.getValue());
		Ext.get("imagedisplay").dom.src = url;
		/* Now adjust the URL */
		uri = String.format('#{0}.{1}.{2}.{3}', stationCB.getValue(),
				varCB.getValue(), ds.format('Y-m-d'), 
				dayInterval.getValue() );
		window.location.href = uri;
		
	}
	
	var form = new Ext.form.FormPanel({
		applyTo		: 'myform',
		labelAlign	: 'top',
		width		: 320,
		style		: 'padding-left: 5px;',
		title		: 'Make Plot Selections Below...',
		items		: [stationCB, varCB, datepicker, dayInterval],
		buttons		: [{
			text	: 'Create Graph',
			handler	: function(){
				updateImage();
				
			}
		}]
	
	});
	/* Check to see if we had something specified on the URL! */
	var tokens = window.location.href.split('#');
	if (tokens.length == 2){
		var tokens2 = tokens[1].split('.');
		if (tokens2.length == 4){
			stationCB.setValue( tokens2[0] );
			varCB.setValue( tokens2[1] );
			datepicker.setValue( tokens2[2] );
			dayInterval.setValue( tokens2[3] );
			updateImage();
		}
	}
});