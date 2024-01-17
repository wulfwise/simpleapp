import time

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.metrics_exporter import OTLPMetricsExporter
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from time import strftime
from flask import Flask, render_template, request, flash, json
from forms import ContactForm
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash

span_exporter = OTLPSpanExporter(
    # optional
    # endpoint:="myCollectorURL:55678",
    # credentials=ChannelCredentials(credentials),
    # metadata=(("metadata", "metadata")),
)
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
span_processor = BatchExportSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

metric_exporter = OTLPMetricsExporter(
    # optional
    # endpoint:="myCollectorURL:55678",
    # credentials=ChannelCredentials(credentials),
    # metadata=(("metadata", "metadata")),
)

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# controller collects metrics created from meter and exports it via the
# exporter every interval
controller = PushController(meter, metric_exporter, 5)

# Configure the tracer to use the collector exporter
tracer = trace.get_tracer_provider().get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


