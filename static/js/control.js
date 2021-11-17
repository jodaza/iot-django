Vue.config.devtools = true

const eventBus = new Vue()

Vue.component('automatico', {
    delimiters: ['!{', '}!'],
    props: {
        intervalos_automatico: {
            type: Array,
            required: true
        }
    },
    template: `
        <div>
            <div>
                <div class="table-responsive text-center">
                    <p class="description">Tabla: intervalos del modo automatico</p>
                    <form @submit.prevent="autoSubmit">
                        <table class="auto_table"  class="table table-hover table-sm ">
                        <thead class="thead-dark">
                            <tr>
                            <th>Sensor</th>
                            <th>Min</th>
                            <th>Max</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(auto, index) in intervalos_automatico" :key="index">
                                <td v-if="auto.sensor == 'temperatura'"> Temperatura </td>
                                <td v-else-if="auto.sensor == 'humedad_aire'"> H.Aire </td>
                                <td v-else-if="auto.sensor == 'suelo1'"> H.suelo #1 </td>
                                <td v-else-if="auto.sensor == 'suelo2'"> H.suelo #2 </td>
                                <td v-else-if="auto.sensor == 'suelo3'"> H.suelo #3 </td>
                                <td v-else-if="auto.sensor == 'suelo4'"> H.suelo #4 </td>
                                <td v-else-if="auto.sensor == 'lux'"> Iluminacion </td>
                                
                                
                                <td>  <input type="number"  id="min_temp" v-model="auto.minimo" placeholder="auto.minimo" ></input> </td>
                                <td>  <input type="number"  id="max_temp" v-model="auto.maximo" placeholder="auto.maximo" ></input> </td>

                            </tr>
                        </TBODY>
                        </table>
                        <button  class="bigButton"   type="submit">Sincronizar</button>
                    </form>
                </div>
            </div>
        </div>
        
        
    
    `,
    data() {
        return {
            hola: null
        }
    },
    methods: {
        autoSubmit() {
            var lista = []
            for (let i = 0; i < this.intervalos_automatico.length; i++) {
                let obj = {}
                let min = this.intervalos_automatico[i]['minimo']
                let max = this.intervalos_automatico[i]['maximo']
                console.info(this.intervalos_automatico)
                obj[this.intervalos_automatico[i].sensor] = {'minimo': min, 'maximo':max}
          
                lista.push(obj)
            }

            eventBus.$emit('autoPut', lista)
        }
    }
})




/* VUE INSTANCE */
var app = new Vue({
    el: '#control_manager',
    delimiters: ["{$", "$}"],
    data: {
        intervalos_automatico: null,
        token: 'Token 49b4ca783a4b68d4b2e163cd5436ce7926d20ad5'
    },
    methods: {

        get_auto_values: function() {
            /* HTTP Headers config */
            let config = {
                headers: {
                    'Authorization' : 'Token 49b4ca783a4b68d4b2e163cd5436ce7926d20ad5',
                    'Content-Type': 'application/json',
                }
              } 
            /* Module Axios to make  HTTP request */
            axios.get('http://127.0.0.1:8000/curl_auto/sensor', config)
            .then(response => {
                this.intervalos_automatico = response.data
                console.log(this.intervalos_automatico)
                })
            .catch(error => console.log(error))
        },
        put_auto_values: function(sen,obj) {
            /* HTTP Headers config */
            let config = {
                headers: {
                    'Authorization' : 'Token 49b4ca783a4b68d4b2e163cd5436ce7926d20ad5',
                    'Content-Type': 'application/json',
                }
              } 
            /* Module Axios to make  HTTP request */
            axios.put('http://127.0.0.1:8000/curl_auto/'+ sen, obj, config)
            .then(response => {
                console.exception('done !!')
                
                })
            .catch(error => console.log(error))
        },

        /* Este metodo sirve para cambiar los modos de numeros a sus respectivos nombres en String */
        modify_values: function(values) {

            for (let i = 0; i < values.length; i++) {
                if(values){
                        if (values[i]['activador'] == 'riego') {
                            this.accriego = values[i]
                        } else {
                            this.accluz = values[i]
                        }
                } 
            };
            this.accriego['change_modo'] = this.mode_to_string(this.accriego['change_modo'])
            this.accluz['change_modo'] = this.mode_to_string(this.accluz['change_modo'])
            console.warn('End async')
        },
        mode_to_string: function(mode) {
            if (mode == 1) {
                return ('programado')
            } else if (mode == 2) {
                return ('manual')
            } else {
                return ('automatico')
            }
                
        }
    },

    created(){
        console.log('Created')
        this.get_auto_values()
        console.log('Created end')
    },
    mounted() {
        console.log('Mounted')
        /*  explicacion */
        eventBus.$on('autoPut', (li) =>{

            for (let i = 0; i < li.length; i++) {
                this.put_auto_values(Object.keys(li[i])[0], li[i][Object.keys(li[i])[0]])
                console.log(this.intervalos_automatico)

            }

        })
    },
})  


