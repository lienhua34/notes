podTemplate(
    cloud: 'dev-cluster',
    namespace: 'kube-system',
    name: 'leh-notes',
    label: 'leh-notes',
    idleMinutes: 1440,
    containers: [
        // jnlp with kubectl
        containerTemplate(
            name: 'jnlp',
            alwaysPullImage: true,
            image: 'cargo.caicloud.io/circle/jnlp:2.62',
            command: '',
            args: '${computer.jnlpmac} ${computer.name}',
        ),
        containerTemplate(
            name: 'nodejs',
            alwaysPullImage: true,
            image: 'cargo.caicloud.io/caicloud/node:6.9.4',
            command: '',
            args: '',
        )
    ]
) {
    node('leh-notes') {
        stage('checkout') {
            checkout scm
        }
        container('nodejs') {
            stage('Compile') {
                sh (
                    """
                    echo BRANCH_NAME: ${BRANCH_NAME}
                    echo BUILD_NUMBER: ${BUILD_NUMBER}
                    echo BUILD_ID: ${BUILD_ID}
                    echo BUILD_DISPLAY_NAME: ${BUILD_DISPLAY_NAME}
                    echo JOB_NAME: ${JOB_NAME}
                    echo JOB_BASE_NAME: ${JOB_BASE_NAME}
                    echo BUILD_TAG: ${BUILD_TAG}
                    echo EXECUTOR_NUMBER: ${EXECUTOR_NUMBER}
                    echo NODE_NAME: ${NODE_NAME}
                    echo NODE_LABELS: ${NODE_LABELS}
                    echo WORKSPACE: ${WORKSPACE}
                    echo JENKINS_HOME: ${JENKINS_HOME}
                    echo JENKINS_URL: ${JENKINS_URL}
                    echo BUILD_URL: ${BUILD_URL}
                    echo JOB_URL: ${JOB_URL}
                    echo currentBuild.number: ${currentBuild.number}
                    echo currentBuild.result: ${currentBuild.result}
                    echo currentBuild.currentResult: ${currentBuild.currentResult}
                    echo currentBuild.displayName: ${currentBuild.displayName}
                    echo currentBuild.id: ${currentBuild.id}
                    echo currentBuild.durationString: ${currentBuild.durationString}
                    echo currentBuild.previousBuild: ${currentBuild.previousBuild}
                    echo currentBuild.nextBuild: ${currentBuild.nextBuild}
                    echo currentBuild.absoluteUrl: ${currentBuild.absoluteUrl}
                    echo currentBuild.buildVariables: ${currentBuild.buildVariables}
                    echo currentBuild.changeSets: ${currentBuild.changeSets}
                    echo currentBuild.rawBuild: ${currentBuild.rawBuild}
                    """
                )
            }
        }
    }
}
