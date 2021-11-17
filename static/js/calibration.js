Vue.config.devtools = true

const eventBus = new Vue()

Vue.config.delimiters = ['!{', '}!'];

Vue.component('table-calibration', {
    delimiters: ['!{', '}!'],
    props: {
        calibration_values: {
            type: Array,
            required: true
        }
    }, 
    data() {
      return {
        count: 0
      }
    },
    template: `
        <div class="table-responsive text-center">
            <form @submit.prevent="sync_submit">
            <table class="auto_table" class="table table-hover table-sm ">
                <thead class="thead-dark">    
                    <tr>
                        <th>Sensor</th>
                        <th>Min</th>
                        <th>Max</th>
                    </tr>
                </thead>
                <tbody>    
                    <tr v-for="(value, index) in calibration_values" :key="index">
                        <td> !{ value.sensor_id }! </td>
                        <td> <input type="number"  id="min_temp" v-model="value.valor_minimo" placeholder="value.valor_minimo" > </input> </td>
                        <td> <input type="number"  id="max_temp" v-model="value.valor_maximo" placeholder="value.valor_maximo" > </input> </td>
                        <p>holaa</p>
                
                
                    </tr>
                <tbody>
            </table>
            <button  class="bigButton"   type="submit">Sincronizar</button>
            </form>
        </div>
    `,
    methods:{
        sync_submit() {
            var lista = []
            for (let i = 0; i < this.calibration_values.length; i++) {
                let obj = {}
                let min = this.calibration_values[i]['valor_minimo']
                let max = this.calibration_values[i]['valor_maximo']
                obj[this.calibration_values[i].sensor_id] = {'valor_minimo': min, 'valor_maximo':max}
                lista.push(obj)
            }
            console.log(lista)
            eventBus.$emit('autoPut', lista)
        }
    },
    mounted() {
        console.log('componente montado')
        console.log(this.calibration_values)
        console.log('!!')
    }
})

var app = new Vue({
    delimiters: ['!{', '}!'],
    el:'#calibracion_sensores',
    data: {
        calibration_values: {},
        real_values: [],
        url_server: 'http://127.0.0.1:8000/',
        calibration_api: 'send_calibration_values/',
        real_values_api: 'send_last_humemdad_values/',
        token: 'df767297ec8cea089c22d07cec40a02890247410',
    },
    

    created() {
        this.get_calibration_values()
 
    },
    mounted() {
        eventBus.$on('autoPut', (li) =>{

            for (let i = 0; i < li.length; i++) {
                this.put_calibration_values(Object.keys(li[i])[0], li[i][Object.keys(li[i])[0]])
                console.log(this.intervalos_automatico)
            }
        })
    },
    methods: {
        get_calibration_values(){
            console.log('getting calibrations values')
            let config = {
                headers: {
                    'Authorization' : 'Token ' + this.token,
                    'Content-Type': 'application/json'
                },
              } 
            /* Module Axios to make  HTTP request */
            axios.get(this.url_server +this.calibration_api+'100/', config)
            .then(response => {
                this.calibration_values = response.data
                console.log(this.calibration_values)
            })
            .catch(error => console.error(error))     
        },
        get_real_values(){
            console.log('getting calibrations values')
            let config = {
                headers: {
                    'Authorization' : 'Token ' + this.token,
                    'Content-Type': 'application/json'
                },
              } 
            /* Module Axios to make  HTTP request */
            axios.get(this.url_server +this.calibration_api+'100/', config)
            .then(response => {
                this.calibration_values = response.data
                console.log(this.calibration_values)
            })
            .catch(error => console.error(error))     
        },
        put_calibration_values(sen, obj){
            console.log('putting calibrations values')
            console.log(obj)
            let config = {
                headers: {
                    'Authorization' : 'Token ' + this.token,
                    'Content-Type': 'application/json'
                },
              } 
            /* Module Axios to make  HTTP request */
            axios.put(this.url_server + this.calibration_api+sen+'/',obj, config)
            .then(response => {
       
                console.log('Done')
            })
            .catch(error => console.error(error))     
        },
        

    }
})