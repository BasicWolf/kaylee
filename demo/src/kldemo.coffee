kl = window.kl

_tasks_counter = 1

$(document).ready( () ->
    kl.console.init('console')
    kl.console.print('<b>Kaylee status console</b><br>')
    kl.node_registered.bind(on_node_registered)
    kl.node_subscribed.bind(on_node_subscribed)
    kl.node_unsubscibed.bind(on_node_unsubscibed)
    kl.project_imported.bind(on_project_imported)
    kl.task_received.bind(on_task_received)
    kl.task_completed.bind(on_task_completed)
    kl.result_sent.bind(on_result_sent)
    kl.client_error.bind(on_client_error)
    kl.log.bind(on_log)
    kl.server_error.bind(on_server_error)
    kl.register()
)

on_node_registered = (data) ->
    apps = data.applications.join(', ')
    app = data.applications[0]
    kl.console.print("Your node is registered by ID
                      <span class='cem'>#{data.node_id}</span>.")
    kl.console.print("Available applications:
                       <span class='cem'>#{apps}</span>.")
    kl.console.print("Subscribing to
                      <span class='cem'>#{app}</span>.")
    kl.subscribe(app)

on_node_subscribed = (config) ->
    sconfig = JSON.stringify(config, null, ' ')
    kl.console.print("Application configuration received:
                      <span class='cem'>#{sconfig}</span>.")

on_node_unsubscibed = (data) ->
    kl.console.print("Node unsubscibed: <span class='cem'>#{data}</span>")

on_project_imported = (app_name) ->
    kl.console.print("Project files imported successfully.")

on_task_received = (data) ->
    kl.console.print("Task [<span class='cem'>id=#{data.id} /
                      ##{_tasks_counter}</span>] received.")

on_task_completed = (data) ->
    kl.console.print("Task [<span class='cem'>##{_tasks_counter}</span>]
                      completed.")
    _tasks_counter += 1

on_result_sent = () ->
    kl.console.print("The result has been sent to the server.")

on_client_error = (e) ->
    kl.console.print("<span class='cerr'>CLIENT ERROR:</span> Line #{e.lineno} in
                      #{e.filename}: #{e.message}")

on_server_error = (message) ->
    kl.console.print("<span class='cerr'>SERVER ERROR: </span> #{message}")

on_log = (message) ->
    kl.console.print("<span class='cem'>LOG:</span> #{message}")