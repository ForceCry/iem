Ext.onReady(function(){

   Ext.ux.grid.filter.StringFilter.prototype.icon = 'find.png';

   var filters = new Ext.ux.grid.GridFilters({
        filters:[
               {type: 'string',  
                dataIndex: 'locations'
                }
                ],
        phpMode:false,
        local:true
        });


    var p = new Ext.Panel({
        title: 'Product Overview',
        collapsible:false,
        width:320,
        height:500,
        items: [Ext.get('controller')]
    });
    p.render('controller-side');


    var expander = new Ext.grid.RowExpander({
        tpl : new Ext.Template(
            '<p><b>Remark:</b> {remark}<br>'
        )
    });


    var ustore = new Ext.data.Store({
          root:'ugcs',
          autoLoad:false,
          proxy: new Ext.data.HttpProxy({
                url: 'json-ugc.php',
                method: 'GET'
          }),
          reader:  new Ext.data.JsonReader({
            root: 'ugcs',
            id: 'id'
           }, [
           {name: 'id'},
           {name: 'ugc'},
           {name: 'name'},
           {name: 'status'},
           {name: 'issue'},
           {name: 'expire'}
          ])
        });


    var jstore = new Ext.data.Store({
          root:'lsrs',
          autoLoad:false,
          proxy: new Ext.data.HttpProxy({
                url: 'json-lsrs.php',
                method: 'GET'
          }),
          reader:  new Ext.data.JsonReader({
            root: 'lsrs',
            id: 'id'
           }, [
           {name: 'id'},
           {name: 'valid'},
           {name: 'type'},
           {name: 'event'},
           {name: 'magnitude'},
           {name: 'city'},
           {name: 'county'},
           {name: 'remark'}
          ])
        });

    var pstore = new Ext.data.Store({
          root:'products',
          autoLoad:false,
          proxy: new Ext.data.HttpProxy({
                url: 'json-list.php',
                method: 'GET'
          }),
          reader:  new Ext.data.JsonReader({
            root: 'products',
            id: 'id'
           }, [
           {name: 'id'},
           {name: 'locations'},
           {name: 'wfo'},
           {name: 'year'},
           {name: 'significance'},
           {name: 'phenomena'},
           {name: 'eventid'},
           {name: 'issued'},
           {name: 'expired'}
          ])
        });

    var jstore2 = new Ext.data.Store({
          root:'lsrs',
          autoLoad:false,
          proxy: new Ext.data.HttpProxy({
                url: 'json-lsrs.php',
                method: 'GET'
          }),
          reader:  new Ext.data.JsonReader({
            root: 'lsrs',
            id: 'id'
           }, [
           {name: 'id'},
           {name: 'valid'},
           {name: 'type'},
           {name: 'event'},
           {name: 'magnitude'},
           {name: 'city'},
           {name: 'county'},
           {name: 'remark'}
          ])
        });



    // create the Grid
    var grid = new Ext.grid.GridPanel({
        id:'lsr-grid',
        store: jstore,
        loadMask: {msg:'Loading Data...'},
        cm: new Ext.grid.ColumnModel([
            expander,
            {header: "Time", sortable: true, dataIndex: 'valid'},
            {header: "Event", width: 100, sortable: true, dataIndex: 'event'},
            {header: "Magnitude", sortable: true, dataIndex: 'magnitude'},
            {header: "City", width: 200, sortable: true, dataIndex: 'city'},
            {header: "County", sortable: true, dataIndex: 'county'}
        ]),
        stripeRows: true,
        title:'Storm Reports within Polygon',
        plugins: expander,
        autoScroll:true
    });

    // create the Grid
    var grid2 = new Ext.grid.GridPanel({
        id:'all-lsr-grid',
        isLoaded:false,
        store: jstore2,
        loadMask: {msg:'Loading Data...'},
        cm: new Ext.grid.ColumnModel([
            expander,
            {header: "Time", sortable: true, dataIndex: 'valid'},
            {header: "Event", width: 100, sortable: true, dataIndex: 'event'},
            {header: "Magnitude", sortable: true, dataIndex: 'magnitude'},
            {header: "City", width: 200, sortable: true, dataIndex: 'city'},
            {header: "County", sortable: true, dataIndex: 'county'}
        ]),
        stripeRows: true,
        title:'All Storm Reports within Time Period',
        plugins: expander,
        autoScroll:true
    });


    // create the Grid
    var grid3 = new Ext.grid.GridPanel({
        id:'ugc-grid',
        store: ustore,
        loadMask: {msg:'Loading Data...'},
        cm: new Ext.grid.ColumnModel([
            {header: "UGC", width: 50, sortable: true, dataIndex: 'ugc'},
            {header: "Name", width: 200, sortable: true, dataIndex: 'name'},
            {header: "Status", width: 50, sortable: true, dataIndex: 'status'},
            {header: "Issue", sortable: true, dataIndex: 'issue'},
            {header: "Expire", sortable: true, dataIndex: 'expire'}
        ]),
        stripeRows: true,
        autoScroll:true,
        title:'Geography Included',
        collapsible: false,
        animCollapse: false
    });

    function myEventID(val, p, record){
        return "<span><a href=\"warnings_cat.phtml?year="+ record.get('year') +"&wfo="+ record.get('wfo') +"&phenomena="+ record.get('phenomena') +"&significance="+ record.get('significance') +"&eventid="+ val +"\">" + val + "</a></span>";
    }

function mySplitter(val) {
    var tokens = val.split(",");
    var s = "";
    for(i=0; i < tokens.length; i++) {
      s += tokens[i] +",";
      if ((i % 3) == 0 && i > 0) s += "<br />";
    }
    return '<span>' + s + '</div>';
}

    // create the Grid
    var grid4 = new Ext.grid.GridPanel({
        id:'products-grid',
        store: pstore,
        width:640,
        loadMask: {msg:'Loading Data...'},
        cm: new Ext.grid.ColumnModel([
          {header: "Event ID", renderer: myEventID, width: 60, sortable: true, dataIndex: 'eventid'},
          {header: "Issued", width: 140, sortable: true, dataIndex: 'issued'},
          {header: "Expired", width: 140, sortable: true, dataIndex: 'expired'},
          {header: "Locations", renderer: mySplitter, width: 300, sortable: true, dataIndex: 'locations'}
        ]),
        plugins: filters,
        stripeRows: true,
        autoScroll:true,
        title:'Other Events',
        collapsible: false,
        animCollapse: false
    });


    var tabs22 = new Ext.TabPanel({
        renderTo: 'displaytabs',
        id: 'top-display',
        width:660,
        height:520,
        plain:true,
        enableTabScroll:true,
        items:[
            {id:'radar-display', contentEl:'radar', title: 'RADAR'},
            grid,
            grid2,
            grid3,
            grid4
         ],
        activeTab: 0
    });

    var tabs = new Ext.TabPanel({
        applyTo: 'tabs1',
        id:'text-display',
        width:800,
        defaults:{autoHeight: true},
        frame:true,
        plain:true,
        enableTabScroll:true,
        deferredRender:false,
        autoTabs:true,
        resizeTabs:false,
        autoScroll:true
  }); 


});

