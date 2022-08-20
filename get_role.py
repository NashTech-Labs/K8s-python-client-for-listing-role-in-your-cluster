from kubernetes import client
from kubernetes.client import ApiClient

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.RbacAuthorizationV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None
def __format_data_for_cluster_role(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for role in json_data["items"]:
                temp_dict={
                    "role": role["metadata"]["name"],  
                    "namespace": role["metadata"]["namespace"],
                }
                temp_list.append(temp_dict)
        return temp_list

def get_role(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            daemonset_list =client_api.list_role_for_all_namespaces(watch=True)
            data=__format_data_for_cluster_role(daemonset_list)
            #print("Daemonset under all namespaces: {}".format(data))
            return data
        else:
            daemonset_list = client_api.list_namespaced_role(namespace)
            data=__format_data_for_cluster_role(daemonset_list)
            #print("Daemonset under default namespaces: {}".format(data))
            print(data)


if __name__ == "__main__":
    cluster_details={
        "bearer_token":"<YOUR_BEARER_TOKEN>",
        "api_server_endpoint":"<YOUR_SERVER_ENDPOINT"

    }
get_role(cluster_details)