let userid
let network
let nodes, edges

var socket = io();

let updateInterval

let container = document.getElementById("vis")
const visOptions = {
    nodes: {
        shape: "dot",
        size: 8,
    },
    edges: {
        color: '#D3D3D3',
        width: 2
    },
    physics: {
        forceAtlas2Based: {
            gravitationalConstant: -26,
            centralGravity: 0.005,
            springLength: 230,
            springConstant: 0.18,
        },
        maxVelocity: 146,
        solver: "forceAtlas2Based",
        timestep: 0.35,
        stabilization: { iterations: 150 },
    },
};

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function initSim() {
    userid = uuidv4()
    socket.emit('init', { userid:  userid});
}

socket.on('init-res', function (data) {
    nodes = new vis.DataSet(data.nodes)
    edges = new vis.DataSet(data.edges)
    network = new vis.Network(container, { nodes: nodes, edges: edges }, visOptions);
})

function updateSim() {
    updateInterval = setInterval(() => {
        console.log("triggered update")
        socket.emit('update', { userid:  userid});
    }, 1000)
}

socket.on('update-res', function (data) {
    nodes.update(data.nodes)
    edges.update(data.edges)
    console.log(data.unlinks)
    edges.remove(data.unlinks)
    // edges.update(data.edges)
    // edges.clear()
    // edges.add(data.edges)
})

function skipSim() {
    clearInterval(updateInterval)
    socket.emit('skip', { userid:  userid});
}

socket.on('skip-res', function (data) {
    nodes.update(data.nodes)
    edges.update(data.edges)
    console.log(data.unlinks)
    edges.remove(data.unlinks)
    // edges.update(data.edges)
    // edges.clear()
    // edges.add(data.edges)
})